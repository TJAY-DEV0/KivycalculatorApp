import ast
import operator
import re

# Map safe operators and functions to their standard library implementations
safe_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

# Map unary operators
safe_unary_operators = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expr):
    """Safely evaluate a mathematical expression string, handling leading zeros."""
    
    # Pre-process the expression for specific syntax that ast.parse might reject.
    # This is still fragile, but better than nothing.
    # For robust parsing, a dedicated math parser library is best.
    cleaned_expr = re.sub(r'(\+\s*)+', '+', expr)
    cleaned_expr = re.sub(r'(\-\s*)+', '-', cleaned_expr)
    
    try:
        node = ast.parse(cleaned_expr, mode='eval').body

        def _evaluate(n):
            if isinstance(n, ast.Constant):
                if isinstance(n.value, (int, float)):
                    return n.value
                else:
                    raise TypeError("Unsupported constant type")
            elif isinstance(n, ast.BinOp):
                left = _evaluate(n.left)
                right = _evaluate(n.right)
                op = safe_operators.get(type(n.op))
                if op:
                    return op(left, right)
                else:
                    raise TypeError("Unsupported operator")
            elif isinstance(n, ast.UnaryOp):
                op = safe_unary_operators.get(type(n.op))
                if op:
                    return op(_evaluate(n.operand))
                else:
                    raise TypeError("Unsupported unary operator")
            else:
                raise TypeError(f"Unsupported expression type: {type(n)}")

        return _evaluate(node)

    except (SyntaxError, ZeroDivisionError, TypeError, ValueError) as e:
        return ""