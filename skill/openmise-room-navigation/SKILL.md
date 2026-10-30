---
name: openmise-room-navigation
description: Plan room-to-room actor movement through evidenced doors and corridors in scanned environments.
---

# 房间与走廊导航

复用[空间证据](../references/spatial-evidence.md)和[人物导航](../openmise-character-navigation/SKILL.md)。
房间名称不是可达性证据，外部总览也不能证明走廊内部通畅。

1. 获取起点房间、门洞两侧、走廊转折和终点的有效视图。
2. 分别确认方向、局部地面、尺度、房间锚点和障碍，记录未知覆盖区域。
3. 将房间/走廊可走区域及门洞连接组成统一地图，核对门洞宽高与人物净空。
4. 使用已确认连接规划路径；不能为了连通而凭空扩大可走区域或忽略墙体。
5. 在门洞、转角、起终点和镜头变化处预览人物全身与相机视线。
6. 扫描、地图或人物尺寸改变后重新检查路线与净空。

遇到楼梯、层间高差、动态障碍或无法确认的地形，说明当前平面模型的限制，
先取得适当几何与运动求解能力再继续相关规划。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
