"""A safe arithmetic evaluator that never executes Python expressions."""

import ast
import operator

from app.tools.registry import RegisteredTool


class Calculator:
    _binary_operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_operations = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    async def calculate(self, expression: str) -> dict[str, float | int]:
        tree = ast.parse(expression, mode="eval")
        result = self._evaluate(tree.body)
        if isinstance(result, complex) or abs(result) > 10**100:
            raise ValueError("The calculation result is outside supported bounds.")
        return {"expression": expression, "result": result}

    def _evaluate(self, node: ast.expr) -> float | int:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._unary_operations:
            return self._unary_operations[type(node.op)](self._evaluate(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in self._binary_operations:
            left, right = self._evaluate(node.left), self._evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 20:
                raise ValueError("Exponents above 20 are not supported.")
            return self._binary_operations[type(node.op)](left, right)
        raise ValueError("Only basic arithmetic expressions are supported.")


def calculator_tool(calculator: Calculator) -> RegisteredTool:
    return RegisteredTool(
        name="calculate",
        description="Perform a basic arithmetic calculation.",
        parameters={
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Arithmetic expression."}},
            "required": ["expression"],
            "additionalProperties": False,
        },
        execute=calculator.calculate,
    )
