# Coordinate systems and matrix conversion conventions

## Matrices and pixels

- World: Blender's right-handed coordinate system, with +Z up. Keep scene length units;
  do not assume they are meters.
- Blender camera: +X right, +Y up, -Z forward. `camera_to_world` is the 4×4 homogeneous
  matrix C, not a world-to-camera matrix.
- Model camera: OpenCV convention, +X right, +Y down, +Z forward.
  `B = diag(1,-1,-1)` converts its directions into Blender camera coordinates.
- JSON matrices contain rows. Multiply column vectors on the left by matrices.
  Points have homogeneous w=1; directions have w=0, so camera translation does not
  contribute to direction conversion.
- Source screenshots are not cropped, resized or rotated. K belongs to the original image.
  Projection `u=fx*x/z+cx, v=fy*y/z+cy` uses OpenCV camera coordinates.
- The top-left image boundary is (0,0); pixel centers are (i+0.5,j+0.5).
  Boxes use pixel boundaries `xyxy=[xmin,ymin,xmax,ymax]` within
  [0,width]×[0,height], not normalized coordinates.
- Masks are single-channel PNGs at the original image resolution: 0 for background,
  255 for foreground. Array indexing is mask[v,u].

Version 1 supports only centered, undistorted perspective cameras with square pixels and
an uncropped frame. Reject orthographic and panoramic cameras. Derive focal lengths from
Blender's projection matrix; the principal point is (width/2,height/2). Camera matrices
must not contain scale, reflection or shear.

## GeoCalib sign convention and fusion

The [official Gravity implementation](https://github.com/cvg/GeoCalib/blob/main/geocalib/gravity.py)
returns `(0,-1,0)` for zero roll and pitch. Despite the field name gravity, this bridge
interprets that vector as **up** in the model camera coordinates defined above, records
`direction_semantics:"up"`, and does not negate it again.

```text
up_world_i = normalize(C_i[:3,:3] @ B @ geocalib_vector_i)
down_world_i = -up_world_i
up_world = normalize(sum(up_world_i))
residual_i = acos(clamp(dot(up_world_i, up_world), -1, 1))
```

Produce an applicable matrix only with at least two valid views and a maximum residual
of 15° or less by default. Retain all directions and residuals. Use equal weights rather
than inventing model confidence scores.
Do not flip opposite directions to agree before averaging; cancellation must return
uncertain. Near-duplicate images cannot replace observations from different angles with
environmental cues. When changing the GeoCalib implementation or adapter, first verify the
vector sign using cameras with known upright and inverted orientations.

## Correction and restoration

Let u be the fused world-up direction and z=(0,0,1). The script uses Rodrigues' formula
to compute the shortest rotation satisfying `R*u=z`.
When u and z are opposite, choose a deterministic perpendicular axis for a 180° rotation.
This axis does not imply north. Gravity never uniquely determines horizontal heading.
For an explicit world-space pivot p, defaulting to the world origin:

```text
T = [[R, p-R*p], [0,0,0,1]]
M_asset_after = T @ M_asset_before
M_asset_before = inverse(T) @ M_asset_after
```

Keep cameras fixed in world space while rotating the asset. If the environment leaves
the frame, reframe the view and record new C/K values.
Transform each top-level asset root once and let the hierarchy propagate the transform
to proxies. Do not rotate both a root and its children. Verify that the plugin transforms
complete Gaussians rather than only their centers.
For each Gaussian, the intended geometry is center `mu'=R*mu+t` and covariance
`Sigma'=R*Sigma*R^T`.
The model helpers do not rewrite PLY attributes or apply Blender transforms. Use an available
renderer that supports whole-asset transforms, and verify anisotropy and view-dependent appearance
through actual rendered images.
Restore saved absolute matrices to avoid accumulated errors from repeatedly applying
inverse transforms.
