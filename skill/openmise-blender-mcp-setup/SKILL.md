---
name: openmise-blender-mcp-setup
description: Set up and verify a user-controlled Blender MCP connection before scene editing.
---

# 连接 Blender MCP

需要能在 Blender 内执行 Python 或场景操作的宿主工具。
可使用 [Blender MCP](https://github.com/ahujasid/blender-mcp)；以其上游说明安装与配置，
本仓库不包含该附加组件或 MCP 服务端。

1. 确认 Blender 可启动，记录实际版本和正在编辑的工程。
2. 在同一 Blender 实例安装并启用兼容的 Blender MCP 附加组件。
3. 根据上游说明在 Agent 宿主配置 MCP 服务，并启动 Blender 中的连接。
   连接参数来自用户环境；不要假定任意端口上的实例就是目标工程。
4. 先执行只读检查：查询 Blender 版本、场景名称、对象列表与活动相机。
5. 确认返回内容属于目标实例，才执行编辑。保存已有工程或工作副本。

连接失败时区分宿主服务未启动、附加组件未启用、端口不匹配和超时。
超时后先核对 Blender 是否仍在运行操作，避免重复提交。
远程执行接口会以 Blender 进程权限运行代码，只连接可信的本机或受控环境。

操作前遵循[共同执行约定](../references/workflow.md)，只使用当前宿主实际可用的工具。
