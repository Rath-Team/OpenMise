---
name: openmise-character-layout
description: Choose character import or generation, then place and verify actors in a Blender scene.
---

# 人物布局工作流

这是人物工作流入口；按资产条件选择分支，不要求同时运行导入与生成。

1. 有人物文件时用[人物导入](../openmise-character-import/SKILL.md)；
   需要程序化白模时用[人物生成](../openmise-character-generate/SKILL.md)。
2. 检查资产层级、骨架、世界高度、朝向与脚底位置。
   骨架存在不证明蒙皮或任意动作兼容；OBJ 本身不含可用骨架。
3. 扫描背景先完成方向、局部支撑、尺度与目标语义位置的确认。
4. 用[场景摆放](../openmise-scene-placement/SKILL.md)定位，分别核对尺寸与取景。
5. 程序化动作用[动作设计](../openmise-motion/SKILL.md)；已有动作用[动作导入](../openmise-motion-import/SKILL.md)。
6. 查看人物全身、脚底、参考物和遮挡关系，再进入镜头与输出阶段。

修复特写构图应调整机位或镜头，不能随意改变角色物理尺寸。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
