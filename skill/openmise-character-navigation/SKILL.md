---
name: openmise-character-navigation
description: Plan actor movement through verified walkable regions and inspect path and animation clearance.
---

# 人物路线与行走

用于同一已确认平面中的命名位置、路径点与简单避障；楼梯、多层和动态避障需要其他求解方法。

1. 将目标锚点、可走区域、障碍、脚底高度和扫描变换置于同一坐标系。
2. 用观察证据确认起终点及连通性，未知区域视为未确认可走。
3. 按角色真实占地及转身姿态保守膨胀障碍，并收缩可走边界。
4. 在有效区域内规划路径；找不到通路时报告原因，不穿墙或缩小人物规避失败。
5. 按路径长度与时长建立运动，区分根对象位移、步态周期和朝向插值。
   停顿、转身与过门动作应有明确时间范围。
6. 检查逐帧脚底、转角和占地，再实际查看关键位置、门口和遮挡变化处的动画预览。

二维圆形占地通过不证明手臂、头部、服饰和全身三维碰撞已通过。
房间间路径另见[房屋导航](../openmise-room-navigation/SKILL.md)。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
