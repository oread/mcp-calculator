# MCP-Tools | MCP工具集

A comprehensive collection of MCP (Model Context Protocol) tools for extending AI capabilities with Dataverse integration, news aggregation, music streaming, calculations, and more.

一个全面的MCP工具集合，通过Dataverse集成、新闻聚合、音乐流媒体、计算等方式扩展AI能力。

## Overview | 概述

MCP (Model Context Protocol) is a protocol that allows servers to expose tools that can be invoked by language models. Tools enable models to interact with external systems, such as querying databases, calling APIs, or performing computations. Each tool is uniquely identified by a name and includes metadata describing its schema.

MCP（模型上下文协议）是一个允许服务器向语言模型暴露可调用工具的协议。这些工具使模型能够与外部系统交互，例如查询数据库、调用API或执行计算。每个工具都由一个唯一的名称标识，并包含描述其模式的元数据。

## Available Tools | 可用工具

### 🧮 Calculator
Mathematical calculations with Python expressions
- Support for math and random modules
- Safe expression evaluation

### 📊 Dataverse
Microsoft Dataverse/Dynamics 365 integration
- OAuth 2.0 client credentials authentication
- Full CRUD operations (Create, Read, Update, Delete)
- OData query support
- Automatic token management

### 📰 VNExpress
Vietnamese news aggregation from VNExpress.net
- Latest news by category
- Search functionality
- Full article content extraction
- Trending news

### 🎵 Zing MP3
Music streaming integration with Zing MP3
- Song search
- Artist and playlist browsing
- Music charts (realtime, weekly, by genre)
- Browser integration

## Features | 特性

- 🔌 Bidirectional communication between AI and external tools | AI与外部工具之间的双向通信
- 🔄 Automatic reconnection with exponential backoff | 具有指数退避的自动重连机制
- 📊 Real-time data streaming | 实时数据流传输
- 🛠️ Easy-to-use tool creation interface | 简单易用的工具创建接口
- 🔒 Secure WebSocket communication | 安全的WebSocket通信
- ⚙️ Multiple transport types support (stdio/sse/http) | 支持多种传输类型（stdio/sse/http）
- 🐳 Docker support for easy deployment | Docker支持，便于部署

## Quick Start | 快速开始

1. Install dependencies | 安装依赖:
```bash
pip install -r requirements.txt
```

2. Set up environment variables | 设置环境变量:
```bash
export MCP_ENDPOINT=ws://192.168.1.11:8004/mcp_endpoint/mcp/?token=jR1BVACU%2B8gb7%2BBgAOqYHwtssGQWvlD%2BQQK4HEdW%2F2dThXgPoaMlcZ%2BA4rp4sl9D

```

3. Run the calculator example | 运行计算器示例:
```bash
python mcp_pipe.py calculator.py
```

Or run all configured servers | 或运行所有配置的服务:
```bash
python mcp_pipe.py
```

*Requires `mcp_config.json` configuration file with server definitions (supports stdio/sse/http transport types)*

*需要 `mcp_config.json` 配置文件定义服务器（支持 stdio/sse/http 传输类型）*

## Project Structure | 项目结构

- `mcp_pipe.py`: Main communication pipe that handles WebSocket connections and process management | 处理WebSocket连接和进程管理的主通信管道
- `calculator.py`: Mathematical calculation tool | 数学计算工具
- `dataverse.py`: Microsoft Dataverse/D365 integration tool | Dataverse/D365集成工具
- `vnexpress.py`: Vietnamese news aggregation tool | 越南新闻聚合工具
- `zingmp3.py`: Music streaming tool | 音乐流媒体工具
- `requirements.txt`: Project dependencies | 项目依赖
- `Dockerfile`: Docker container configuration | Docker容器配置
- `docker-compose.yml`: Docker Compose orchestration | Docker Compose编排

## Config-driven Servers | 通过配置驱动的服务

编辑 `mcp_config.json` 文件来配置服务器列表（也可设置 `MCP_CONFIG` 环境变量指向其他配置文件）。

配置说明：
- 无参数时启动所有配置的服务（自动跳过 `disabled: true` 的条目）
- 有参数时运行单个本地脚本文件
- `type=stdio` 直接启动；`type=sse/http` 通过 `python -m mcp_proxy` 代理

## Creating Your Own MCP Tools | 创建自己的MCP工具

Here's a simple example of creating an MCP tool | 以下是一个创建MCP工具的简单示例:

```python
from fastmcp import FastMCP

mcp = FastMCP("YourToolName")

@mcp.tool()
def your_tool(parameter: str) -> dict:
    """Tool description here"""
    # Your implementation
    return {"success": True, "result": result}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Use Cases | 使用场景

- Mathematical calculations | 数学计算
- Dataverse/Dynamics 365 data management | Dataverse/Dynamics 365数据管理
- News monitoring and aggregation | 新闻监控和聚合
- Music discovery and streaming | 音乐发现和流媒体
- Data processing and analysis | 数据处理和分析
- Custom tool integration | 自定义工具集成

## Docker Deployment | Docker部署

### Build and Run with Docker

```bash
# Build the image
docker build -t mcp-tools .

# Run a specific tool
docker run -e MCP_ENDPOINT="your-endpoint-url" mcp-tools calculator.py

# Run with docker-compose
docker-compose up -d
```

### Environment Variables

- `MCP_ENDPOINT`: WebSocket endpoint URL (required)
- `DATAVERSE_URL`: Dataverse organization URL (for Dataverse tool)
- `CLIENT_ID`: Azure AD client ID (for Dataverse tool)
- `CLIENT_SECRET`: Azure AD client secret (for Dataverse tool)
- `TENANT_ID`: Azure AD tenant ID (for Dataverse tool)

## Requirements | 环境要求

- Python 3.7+
- websockets>=11.0.3
- python-dotenv>=1.0.0
- mcp>=1.8.1
- pydantic>=2.11.4
- mcp-proxy>=0.8.2

## Contributing | 贡献指南

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献代码！请随时提交Pull Request。

## License | 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用MIT许可证 - 详情请查看LICENSE文件。

## Acknowledgments | 致谢

- Thanks to all contributors who have helped shape this project | 感谢所有帮助塑造这个项目的贡献者
- Inspired by the need for extensible AI capabilities | 灵感来源于对可扩展AI能力的需求
