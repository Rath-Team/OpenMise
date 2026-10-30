---
name: openmise-3dgs-addon-setup
description: Prepare a Blender addon capable of importing and rendering Gaussian splats.
---

# 安装 3DGS 附加组件

3DGS PLY 需要高斯渲染支持；普通网格导入器不能保留完整高斯外观。
可使用 [KIRI 3DGS Render](https://github.com/Kiri-Innovation/3dgs-render-blender-addon)。

1. 按附加组件上游说明选择与当前 Blender 兼容的发行包，检查其许可证。
2. 在目标 Blender 实例安装、启用，并确认相关操作和面板实际存在。
3. 用用户提供的小型测试 PLY 增量导入，检查对象、可见高斯、材质和渲染输出。
4. 核对可用 GPU、图形上下文与显存。某些高斯渲染路径需要 GUI/图形上下文；
   不把普通网格的后台渲染成功视作高斯渲染可用。
5. 渲染一个实际预览，确认图像非空且与视口预期一致，之后再处理完整扫描。

组件安装成功与扫描格式兼容是两项独立检查。
模型权重、人物素材和附加组件均由使用者按各自许可另行获取。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
