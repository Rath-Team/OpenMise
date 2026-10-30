"""Grounding DINO pixel boxes and optional SAM 2 masks; no inferred XYZ."""
from pathlib import Path
from common import cli, read, validate_views


def execute(req):
    import numpy as np
    import torch
    from PIL import Image, ImageDraw
    from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
    capture = read(req["views_path"])
    views = validate_views(capture)
    query = req["query"].strip().lower().rstrip(".") + "."
    if query == ".":
        raise ValueError("nonempty query required")
    device = req.get("device", "cpu")
    model_id = req.get("model", "IDEA-Research/grounding-dino-tiny")
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device).eval()
    predictor = None
    if req.get("sam2_checkpoint") or req.get("sam2_config"):
        from sam2.build_sam import build_sam2
        from sam2.sam2_image_predictor import SAM2ImagePredictor
        predictor = SAM2ImagePredictor(build_sam2(req["sam2_config"], req["sam2_checkpoint"], device=device))
    out = Path(req["output_dir"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    detections, overlays = [], []
    for v in views:
        image = Image.open(v["image_path"]).convert("RGB")
        if image.size != (v["width"], v["height"]):
            raise ValueError("image size differs from capture metadata")
        inputs = processor(images=image, text=query, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = model(**inputs)
        result = processor.post_process_grounded_object_detection(
            outputs, inputs.input_ids, threshold=float(req.get("box_threshold", 0.4)),
            text_threshold=float(req.get("text_threshold", 0.3)), target_sizes=[image.size[::-1]])[0]
        boxes = result["boxes"].detach().cpu().numpy()
        scores = result["scores"].detach().cpu().tolist()
        labels = result.get("text_labels", result.get("labels"))
        if not all(isinstance(label, str) for label in labels):
            raise ValueError("processor must return text labels; check Transformers version")
        boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, image.width)
        boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, image.height)
        masks = None
        if predictor and len(boxes):
            with torch.inference_mode():
                predictor.set_image(np.array(image))
                masks, _, _ = predictor.predict(point_coords=None, point_labels=None, box=boxes, multimask_output=False)
            masks = np.asarray(masks).reshape(-1, image.height, image.width)
            if len(masks) != len(boxes):
                raise ValueError("SAM 2 returned mismatched mask count")
        draw = ImageDraw.Draw(image)
        for index, (box, score, label) in enumerate(zip(boxes, scores, labels)):
            if not np.isfinite(box).all() or box[2] <= box[0] or box[3] <= box[1]:
                continue
            candidate = f"{v['view_id']}-{index}"
            mask_path = None
            if masks is not None:
                mask_path = str(out / (candidate + "-mask.png"))
                Image.fromarray((masks[index] > 0).astype("uint8") * 255).save(mask_path)
            draw.rectangle(box.tolist(), outline="red", width=3)
            draw.text((float(box[0]), float(box[1])), str(index), fill="red")
            detections.append({"candidate_id": candidate, "name": label, "view_id": v["view_id"],
                               "image_path": v["image_path"], "bbox_xyxy": box.tolist(), "box_units": "pixels",
                               "score": float(score), "mask_path": mask_path,
                               "evidence": {"model": model_id, "query": query, "score": float(score)}})
        overlay = str(out / (v["view_id"] + "-boxes.png"))
        image.save(overlay)
        overlays.append({"view_id": v["view_id"], "image_path": overlay})
    return {"status": "success" if len(detections) == 1 else "uncertain", "state_id": capture["state_id"],
            "detections": detections, "overlays": overlays, "coverage": "supplied_views_only",
            "reason": "single_candidate" if len(detections) == 1 else "multiple_candidates" if detections else "not_visible_in_supplied_views",
            "next_action": "switch_view" if len(detections) == 1 else "select_candidate" if detections else "capture_more_views",
            "instance_fusion": False}


if __name__ == "__main__":
    raise SystemExit(cli(execute))
