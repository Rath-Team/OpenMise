---
name: openmise-output
description: Save Blender projects, render reviewed frames and encode image sequences into video.
---

# 预览、工程与视频输出

先确认输出目录、活动相机、时间范围、帧率、分辨率和文件覆盖行为。
输出默认放在用户指定的工作目录，不把视频、资产或日志写回技能目录。

1. 保存可编辑 `.blend` 工作副本，核对外部纹理和链接资产的可用性。
2. 渲染动作边界、接触、遮挡和镜头变化附近的实际图片，并查看后再启动全序列。
3. 渲染图像序列，核对每一帧存在且尺寸正确。超时后先核对已有输出和进程，不重复启动渲染。
4. 使用本机 FFmpeg 编码，按实际序列设置起始编号与帧率。示例仅适用于从 1 开始的六位 PNG：

```sh
ffmpeg -framerate 24 -start_number 1 -i frames/%06d.png -c:v libx264 -pix_fmt yuv420p clip.mp4
```

5. 使用 FFprobe 或可用媒体工具检查实际时长、分辨率、帧率和可解码帧数，
   再查看最终视频的关键帧。编码完成不等于动作、接触与画面质量达标。
6. 返回真实存在的工程/图片/视频路径，说明完成范围和未验证事项。

偶数画幅适合上述 yuv420p 示例。无 GPU 图形上下文时，先确认选用的高斯渲染器是否支持该执行方式。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
