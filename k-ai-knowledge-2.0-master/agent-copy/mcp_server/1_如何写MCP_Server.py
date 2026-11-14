# 1.导入 FastMCP
from mcp.server.fastmcp import FastMCP

# 2.创建 MCP Server 对象
mcp = FastMCP(name="weather")

# 3. 注册工具
@mcp.tool()
def get_current_weather(city: str) -> str:
    """
    获取指定城市的当前天气
    :param city: 城市地址
    :return: 天气信息
    """
    return f"{city}: 100°C, 风速 0km/h, 天气状况: ☀️ 超级热"

# 4.启动 MCP Server
if __name__ == '__main__':
    mcp.run(transport="stdio")

