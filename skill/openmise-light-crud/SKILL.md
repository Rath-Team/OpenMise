---
name: openmise-light-crud
description: Create and edit point, sun, spot and area lights in Blender.
---

# 灯光对象管理

检查现有灯光、世界环境与当前渲染器，避免重复堆叠灯导致曝光失控。

1. 按需要创建 Point、Sun、Spot 或 Area，并赋予可识别名称。
2. 设置位置、朝向、颜色与能量。Sun 的方向有效，位置不控制物理距离衰减。
3. Area 的面积影响光源外观和阴影软硬；Spot 还需设置角度与边缘过渡。
4. 分清隐藏、禁用渲染和删除；共享数据块的编辑可能影响其他灯对象。
5. 渲染局部预览检查阴影、过曝与材质响应，再调整能量或尺寸。

灯类型的能量单位与渲染效果不同，不直接以同一数值互换。
完整布光意图见[灯光设计](../openmise-lighting/SKILL.md)。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
