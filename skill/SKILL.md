---
name: openmise
description: Guide Blender scene construction, scanned-scene understanding, character placement, motion, camera work, lighting and verified local video output. Route requests to focused topic guides using the host agent's available Blender tools.
---

# OpenMise

按任务加载一个主题，复用已验证的场景状态。开始前阅读[共同执行约定](references/workflow.md)。
本技能提供工作流与可选模型辅助脚本；Blender 执行由宿主已有工具完成。
先查询工具能力，不能把本技能名称当作已注册的可调用工具。

| 任务 | 主题 |
|---|---|
| 白模场景与动画 | [openmise-builder](openmise-builder/SKILL.md) |
| 复杂场景生成与修正 | [openmise-generated-scene](openmise-generated-scene/SKILL.md) |
| 连接 Blender MCP | [openmise-blender-mcp-setup](openmise-blender-mcp-setup/SKILL.md) |
| 安装 3DGS 附加组件 | [openmise-3dgs-addon-setup](openmise-3dgs-addon-setup/SKILL.md) |
| 网格管理 | [openmise-mesh-crud](openmise-mesh-crud/SKILL.md) |
| 3DGS 资产管理 | [openmise-3dgs-crud](openmise-3dgs-crud/SKILL.md) |
| 扫描观察与空间校准 | [openmise-scene-understanding](openmise-scene-understanding/SKILL.md) |
| 人物布局工作流 | [openmise-character-layout](openmise-character-layout/SKILL.md) |
| 人物资产导入 | [openmise-character-import](openmise-character-import/SKILL.md) |
| 程序化人物生成 | [openmise-character-generate](openmise-character-generate/SKILL.md) |
| 人物与资产摆放 | [openmise-scene-placement](openmise-scene-placement/SKILL.md) |
| 人物路线与行走 | [openmise-character-navigation](openmise-character-navigation/SKILL.md) |
| 房间与走廊导航 | [openmise-room-navigation](openmise-room-navigation/SKILL.md) |
| 姿态与程序化动作 | [openmise-motion](openmise-motion/SKILL.md) |
| 动作导入与重定向 | [openmise-motion-import](openmise-motion-import/SKILL.md) |
| 相机管理与构图 | [openmise-camera-crud](openmise-camera-crud/SKILL.md) |
| 镜头语言与景深 | [openmise-cinematography](openmise-cinematography/SKILL.md) |
| 跟拍与运动镜头 | [openmise-camera-motion](openmise-camera-motion/SKILL.md) |
| 灯光对象管理 | [openmise-light-crud](openmise-light-crud/SKILL.md) |
| 自然语言布光 | [openmise-lighting](openmise-lighting/SKILL.md) |
| 预览、工程与视频输出 | [openmise-output](openmise-output/SKILL.md) |
| 3DGS 方向与可见物体识别 | [blender-3dgs](blender-3dgs/SKILL.md) |

典型组合：人物导入或生成 → 场景摆放 → 动作设计或导入 → 镜头/灯光 → 预览与输出。
扫描背景先确认可用观察、方向、局部支撑、尺度和语义锚点，再做放置与路线。
方向与二维识别不能代替三维校准、碰撞检查和视觉验收。

新场景可用米制、Z 向上；编辑现有场景保留其单位并显式换算。
数值验证、语义证据、视觉检查与文件生成状态分别报告。
无图像能力时如实保留待检查状态；工具执行成功不能证明画面符合要求。
