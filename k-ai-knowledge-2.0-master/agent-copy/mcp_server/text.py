from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "database",
    host="127.0.0.1",
    port=8000,
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    mcp.run(transport="streamable-http")