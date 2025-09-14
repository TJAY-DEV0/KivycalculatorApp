import ast
import operator
import re
import math

# Map safe binary operators
safe_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

# Map safe unary operators
safe_unary_operators = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Map safe function calls and constants
safe_functions = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'sqrt': math.sqrt,
    'radians': math.radians,
    'degrees': math.degrees,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'pi': math.pi, 
}

def safe_eval(expr):
    """Safely evaluate a mathematical expression string."""
    
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
            elif isinstance(n, ast.Call):
                func_name = n.func.id if isinstance(n.func, ast.Name) else None
                args = [_evaluate(arg) for arg in n.args]
                
                if func_name in safe_functions and callable(safe_functions[func_name]):
                    return safe_functions[func_name](*args)
                else:
                    raise TypeError("Unsupported function call")
            elif isinstance(n, ast.Name):
                # Handles constants like 'pi'
                if n.id in safe_functions:
                    return safe_functions[n.id]
                else:
                    raise TypeError("Unsupported variable")
            else:
                raise TypeError(f"Unsupported expression type: {type(n)}")

        return _evaluate(node)

    except (SyntaxError, ZeroDivisionError, TypeError, ValueError) as e:
        return ""