---
name: openmise-builder
description: Build Blender blockout scenes and short animations from a natural-language brief.
---

# 白模场景与动画

把需求拆成对象、尺寸、位置、动作时间轴、镜头和输出要求。明确帧率、时长与帧范围；
例如 24 fps 的 5 秒视频使用 1–120 帧，所有动作与切镜使用同一时间约定。

1. 新场景采用米制、Z 轴向上；编辑现有工程时先检查单位和已有内容。
2. 用基础几何建立空间关系，以唯一名称标识人物和道具。灰白材质用于预演，不能把扫描高斯视作可碰撞白模网格。
3. 为站立、行走、转身、抬手等动作建立明确起止帧，保持骨长与道具身份一致。
   道具抓取/交接应记录相对变换与所有权变化，不用物体瞬移掩盖接触问题。
4. 先检查静态布局、全身比例与支撑，再检查动作边界、转身、接触和切镜附近的真实预览。
5. 修改后重新检查受影响的帧，通过后从同一工程渲染视频并保存 `.blend`。

超出简单动作时使用[生成场景](../openmise-generated-scene/SKILL.md)。
含扫描背景时先完成[空间校准](../openmise-scene-understanding/SKILL.md)。
本技能没有固定动作模板执行器；由宿主 Agent 使用可用 Blender 工具实现。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
