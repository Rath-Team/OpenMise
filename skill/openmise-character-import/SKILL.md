---
name: openmise-character-import
description: Import character models and inspect hierarchy, materials and rigs before animation.
---

# 人物资产导入

支持程度取决于用户安装的 Blender 导入器。GLB/glTF、FBX、OBJ、`.blend` 与 PMX 的能力不同。
本技能不包含模型下载服务或自动高质量绑骨服务。

1. 目录输入先列出模型文件，选择具体资产；保持纹理和使用说明的相对目录。
2. 记录现有对象，导入到独立集合或共同根对象下。`.blend` 使用 append/link，
   不通过打开源工程替换当前场景。
3. 检查骨架数量、蒙皮关联、骨骼名称、形态键、材质和缺失纹理。
   多骨架时明确动作目标，不能默认选取第一个骨架。
4. 根据源单位和实际需求统一根对象的尺度与朝向，不独立移动蒙皮子网格。
   米制高度与场景单位的关系为 `world_height = metres / scale_length`。
5. PMX 需要目标 Blender 中兼容的 MMD Tools；检查原始骨架、形态键和纹理。
   导入刚体/关节不等于物理模拟已经构建、烘焙或验证。
6. 渲染预览核对外观和脚底，再交给场景摆放与动作导入主题。

导入失败时撤销本次新建对象，保留原场景。静态网格不能作为已可动画人物交付。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
