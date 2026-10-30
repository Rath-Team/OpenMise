# 可选模型脚本：依赖、输入与执行

这三个脚本只处理已采集图像，不连接 Blender、不应用变换，也不提供渲染器。
取图、保存相机矩阵、应用与恢复变换由用户现有 Blender 工具完成。
`common.py` 仅提供本目录共用的 JSON 读写与视图检查。

## 依赖

- `understand_scene.py`：Python 3.10+ 标准库；用户已配置的兼容视觉服务与模型。
- `estimate_up.py`：NumPy、PyTorch、[GeoCalib](https://github.com/cvg/GeoCalib) 及所需权重。
- `locate_object.py`：NumPy、PyTorch、Pillow、Transformers 和 Grounding DINO 权重；
  可选 [SAM 2](https://github.com/facebookresearch/sam2) 与其配置、权重，用于掩码。

在用户选择的独立虚拟环境按上游项目说明安装依赖，勿替换 Blender 的内置 Python。
GPU 与依赖版本需适配实际环境。模型加载可能下载权重，事先设置模型缓存目录，
按需使用 `HF_HOME`、`TORCH_HOME` 等环境变量避免占用系统盘。
本仓库不分发权重，权重和上游包的许可证独立适用。
没有权重或依赖时不要宣称对应模型已运行；模型版本/API 变化可能需要适配。

## 视图记录

创建 `views.json`。`image_path` 必须为真实图片绝对路径，矩阵为行列表。
下例为格式示意，路径、矩阵、尺寸和身份应替换成实际采集值；方向融合至少需要两个不同视角。

```json
{
  "state_id": "capture-001",
  "phase": "before",
  "asset_matrices": {"ScanRoot": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]},
  "views": [{
    "view_id": "view-001",
    "image_path": "/absolute/path/to/view.png",
    "width": 1280,
    "height": 720,
    "camera_frame": "blender_camera",
    "pixel_coordinates": "xy_top_left_pixels",
    "camera_to_world": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
  }]
}
```

使用居中、无畸变、无缩放/反射的透视相机和未裁剪图像。
`phase` 为 before/after，资产变换后重新采集。
`state_id` 标识同一工作快照，`view_id` 在记录内唯一。坐标约定见 [coordinates.md](coordinates.md)。
脚本的格式检查不证明这些元数据真实可靠，采集者须保证其与实际图像一致。

## 请求

将实际参数写到工作目录中的 JSON 文件，从仓库根目录运行对应命令。
`views_path`、输出目录、模型路径均应指向用户自己的工作文件。

估计方向请求 `estimate-request.json`：

```json
{"views_path":"views.json","device":"cpu","pivot_world":[0,0,0],"max_deviation_deg":15}
```

```sh
python skill/blender-3dgs/scripts/estimate_up.py --request estimate-request.json --output up.json
```

视觉描述请求 `vision-request.json`：

```json
{"views_path":"views.json","endpoint":"https://vision.example/v1","model":"YOUR_VISION_MODEL","api_key_env":"VLM_API_KEY","question":"Describe visible floor, ceiling and objects.","timeout":120}
```

示例域名不是服务地址。用真实服务地址替换，在环境变量 `VLM_API_KEY` 中设置凭据，
不要把密钥写进请求文件或仓库。可添加 `estimate_path` 指向 `up.json` 核对方向。
此命令会将所有输入图片发送到配置的服务，运行前确认该服务适合处理这些图片。

```sh
python skill/blender-3dgs/scripts/understand_scene.py --request vision-request.json --output scene.json
```

二维检测请求 `detect-request.json`：

```json
{"views_path":"views.json","query":"chair","device":"cpu","output_dir":"detections"}
```

可选字段 `sam2_config` 与 `sam2_checkpoint` 必须同时对应可用的 SAM 2 配置和权重。

```sh
python skill/blender-3dgs/scripts/locate_object.py --request detect-request.json --output objects.json
```

退出码：0 表示脚本成功，1 表示失败，2 表示不确定；始终读取 JSON 的状态、依据和限制。
方向估计返回修正矩阵与逆矩阵，但不修改 Blender。检测返回二维像素框/掩码与 view_id，
单个候选的 success 不等于识别事实已经视觉确认，更不等于得到三维位置。
所有生成图片、请求与结果放在独立工作目录，勿提交用户图像、凭据或运行结果。
