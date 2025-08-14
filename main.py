from mcp.server.fastmcp import FastMCP
from typing import Union

# 创建一个 MCP 服务器实例，名称为 "calculator"
mcp = FastMCP("calculator")

@mcp.tool()
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Adds two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.
    """
    return a + b

@mcp.tool()
def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Subtracts the second number from the first.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The difference of a and b.
    """
    return a - b

@mcp.tool()
def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiplies two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The product of a and b.
    """
    return a * b

@mcp.tool()
def divide(a: Union[int, float], b: Union[int, float]) -> Union[str, float]:
    """
    Divides the first number by the second.

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        The quotient of a and b, or an error message if b is zero.
    """
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

if __name__ == "__main__":
    print("Calculator MCP server started. Waiting for Cursor to connect...")
    mcp.run(transport="stdio")