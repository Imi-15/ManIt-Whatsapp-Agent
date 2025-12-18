"""
tools/calculator.py - Calculator Tool
Safely evaluates mathematical expressions.
"""

import math
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> float:
    """
    Safely evaluate a basic arithmetic expression and return the result.
    Supports basic math operations and common math functions.
    
    Example inputs:
    - "2 + 3 * (4 - 1)"
    - "sqrt(16) + pow(2, 3)"
    - "sin(3.14159 / 2)"
    
    Args:
        expression: A mathematical expression as a string
        
    Returns:
        The numerical result as a float
    """
    # Only allow safe math functions
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed_names["__builtins__"] = {}

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"Could not evaluate expression: {expression}. Error: {e}")

    if not isinstance(result, (int, float)):
        raise ValueError(f"Expression did not return a number: {expression}")

    return float(result)
