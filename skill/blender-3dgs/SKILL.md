---
name: blender-3dgs
description: Estimate scan up directions, inspect visible scenes and locate image-space object candidates.
---

# 3DGS 方向与可见物体识别

适用于扫描朝向、可见场景描述及二维目标定位。
采用观察 → 模型判断 → 坐标换算 → Blender 操作 → 真实复核流程。
模型辅助脚本位于本目录 `scripts/`，无需 OpenMise 运行时；Blender 取图与变换由宿主工具完成。

1. 保存资产根矩阵、当前相机、帧和渲染设置，采集至少两个有方向线索的不同视角。
   按[脚本输入与依赖](references/tools.md)生成视图记录。
2. 需要估计向上方向时运行 `estimate_up.py`；核对 GeoCalib 方向符号和相机坐标约定，
   详见[坐标](references/coordinates.md)。方向冲突或线索不足时保留 uncertain。
3. 实际看图核对地面/天花板/天空；可选 `understand_scene.py` 调用用户配置的视觉服务。
   该脚本会把输入图片发送到配置的 endpoint。
4. 方向与视觉证据一致后，将估计的刚体变换作用于完整资产根一次。
   不同时旋转父子对象；确认插件处理高斯协方差和外观。保存原矩阵供恢复。
5. 校正后重新取图和估计，检查形状、地面与场景可读性。重力不决定水平朝向或真实尺度。
6. 找物体可运行 `locate_object.py`，保留 view_id、像素框、分数和可选掩码。
   多候选交由实际观察消歧。无检测仅表示所给视图未发现，不能宣称全场景不存在。

二维框/掩码不是三维锚点，也不自动融合跨视图实例。回到匹配视角前核对资产姿态未改变。
需要人物摆放或导航时继续执行空间校准工作流。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
