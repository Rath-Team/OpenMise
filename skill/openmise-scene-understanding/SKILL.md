---
name: openmise-scene-understanding
description: Inspect scanned scenes, establish scale and support evidence, and record spatial regions.
---

# 扫描观察与空间校准

按需建立六类独立事实：可用观察、向上方向、局部支撑、尺度、语义锚点、可达区域。
一项通过不代表其他项成立，二维识别不能直接产生可靠三维坐标。

1. 增量导入扫描并记录原始到当前世界坐标的变换。
2. 获取总览、内部与局部视图，保存相机矩阵、图像尺寸与视图身份。
   外部墙面遮住室内时换内部机位；重复远景不能证明局部支撑或门洞。
3. 几何平面或 PCA 仅作地面候选；用多视图或用户确认判定真实方向与支撑。
4. 用独立已知尺寸建立尺度，区分 measured、estimated 与 unknown。
   不用待放入人物的假定身高反向证明扫描已经米制标定。
5. 记录房间、门洞、桌面、障碍与可走区域，并引用实际视图/测量。
   语义名称来自观察，不来自文件名或用户提到的搜索目标。
6. 将区域和锚点绑定到同一世界坐标及扫描变换；扫描变动后重审空间数据。

详见[空间证据](../references/spatial-evidence.md)。未知尺度可继续识别，
但不能据此宣称精确米制摆放、净空或通行能力。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
