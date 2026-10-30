"""GeoCalib inference and signed world-up fusion; no Blender dependency."""
import numpy as np
from common import cli, read, validate_views


def unit(vector):
    a = np.asarray(vector, dtype=float)
    if a.shape != (3,) or not np.isfinite(a).all() or np.linalg.norm(a) < 1e-8:
        raise ValueError("expected finite nonzero 3-vector")
    return a / np.linalg.norm(a)


def rotation_to_z(up):
    a, b = unit(up), np.array([0., 0., 1.])
    c = float(np.clip(a @ b, -1, 1))
    if c > 1 - 1e-10:
        return np.eye(3)
    if c < -1 + 1e-10:
        axis = unit(np.cross(a, np.eye(3)[np.argmin(np.abs(a))]))
        return 2 * np.outer(axis, axis) - np.eye(3)
    v = np.cross(a, b)
    x, y, z = v
    K = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return np.eye(3) + K + K @ K / (1 + c)


def fuse(directions, max_deviation_deg=15):
    vectors = np.array([unit(v) for v in directions])
    resultant = float(np.linalg.norm(vectors.mean(axis=0)))
    if resultant < 1e-8:
        return {"status": "uncertain", "reason": "opposed_directions", "resultant": resultant}
    up = unit(vectors.mean(axis=0))
    residuals = np.rad2deg(np.arccos(np.clip(vectors @ up, -1, 1)))
    return {"status": "success" if len(vectors) >= 2 and max(residuals) <= max_deviation_deg else "uncertain",
            "world_up": up.tolist(), "frame": "blender_world", "resultant": resultant,
            "residuals_deg": residuals.tolist(), "max_deviation_deg": float(max(residuals))}


def execute(req):
    import torch
    from geocalib import GeoCalib
    capture = read(req["views_path"])
    views = validate_views(capture)
    device = req.get("device", "cpu")
    model = GeoCalib(weights=req.get("weights", "pinhole")).to(device).eval()
    observations, directions = [], []
    for v in views:
        C = np.asarray(v["camera_to_world"], dtype=float)
        if C.shape != (4, 4) or not np.isfinite(C).all() or not np.allclose(C[3], [0, 0, 0, 1]) or not np.allclose(C[:3, :3].T @ C[:3, :3], np.eye(3), atol=1e-5) or not np.isclose(np.linalg.det(C[:3, :3]), 1):
            raise ValueError("camera_to_world must be rigid")
        with torch.inference_mode():
            prediction = model.calibrate(model.load_image(v["image_path"]).to(device))
        # GeoCalib from_rp(0,0)=(0,-1,0): its vector is UP in x-right/y-down/z-forward.
        raw = unit(prediction["gravity"].vec3d.detach().cpu().numpy().reshape(3))
        world_up = unit(C[:3, :3] @ np.diag([1., -1., -1.]) @ raw)
        directions.append(world_up)
        observations.append({"view_id": v["view_id"], "image_path": v["image_path"],
                             "geocalib_vector": raw.tolist(), "frame": "opencv_camera", "direction_semantics": "up",
                             "world_up": world_up.tolist(), "world_down": (-world_up).tolist(), "weight": 1.0})
    threshold = float(req.get("max_deviation_deg", 15))
    if not 0 < threshold <= 45:
        raise ValueError("max_deviation_deg must be in (0,45]")
    result = {**fuse(directions, threshold), "state_id": capture["state_id"], "phase": capture["phase"],
              "view_ids": [v["view_id"] for v in views], "observations": observations, "yaw_determined": False,
              "asset_matrices": capture["asset_matrices"]}
    if result["status"] == "success":
        R = rotation_to_z(result["world_up"])
        pivot = np.asarray(req.get("pivot_world", [0, 0, 0]), dtype=float)
        if pivot.shape != (3,) or not np.isfinite(pivot).all():
            raise ValueError("invalid pivot_world")
        T = np.eye(4)
        T[:3, :3], T[:3, 3] = R, pivot - R @ pivot
        result.update(correction_matrix=T.tolist(), inverse_matrix=np.linalg.inv(T).tolist(), pivot_world=pivot.tolist(),
                      upright_error_deg=float(np.rad2deg(np.arccos(np.clip(unit(result["world_up"])[2], -1, 1)))))
    else:
        result["candidates_world_up"] = [v.tolist() for v in directions]
        result["next_action"] = "capture_more_views_or_select_ground_normal"
    return result


if __name__ == "__main__":
    raise SystemExit(cli(execute))
