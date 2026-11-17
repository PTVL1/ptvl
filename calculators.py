"""Bounded arithmetic and color harmonies for the classroom tools."""
import ast
import colorsys
import math
import operator


def calculate(expression):
    if len(expression) > 200:
        raise ValueError("Usa uma expressão com até 200 caracteres.")
    tree = ast.parse(expression.replace(",", "."), mode="eval")
    if len(list(ast.walk(tree))) > 80:
        raise ValueError("Simplifica a expressão.")
    operations = {ast.Add: operator.add, ast.Sub: operator.sub,
                  ast.Mult: operator.mul, ast.Div: operator.truediv,
                  ast.Mod: operator.mod}

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = node.value
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1)
        elif isinstance(node, ast.BinOp) and type(node.op) in operations:
            value = operations[type(node.op)](visit(node.left), visit(node.right))
        else:
            raise ValueError("Usa apenas números, parênteses e os operadores +, -, *, / ou %.")
        if abs(value) > 1e15 or not math.isfinite(value):
            raise ValueError("O resultado excede o limite de cálculo (10¹⁵).")
        return value

    return visit(tree.body)


HARMONIES = {
    "Complementar": ([0, 180], "Duas cores opostas no círculo RGB: uma combinação com contraste de matiz."),
    "Análoga": ([0, -30, 30], "Cores vizinhas, separadas por 30°: uma combinação próxima e coesa."),
    "Triádica": ([0, 120, 240], "Três matizes igualmente espaçados: distribui a cor por três famílias."),
    "Complementar dividida": ([0, 150, 210], "A cor de base e as duas vizinhas da sua complementar."),
    "Monocromática": ([0, 0, 0, 0], "Uma só matiz com diferentes luminosidades: explora claros e escuros."),
}


def harmony(base, scheme):
    rgb = tuple(int(base[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hue, lightness, saturation = colorsys.rgb_to_hls(*rgb)
    offsets, explanation = HARMONIES[scheme]
    colors = []
    for index, offset in enumerate(offsets):
        light = [lightness, .22, .65, .88][index] if scheme == "Monocromática" else lightness
        values = colorsys.hls_to_rgb((hue + offset / 360) % 1, light, saturation)
        colors.append("#" + "".join(f"{round(v * 255):02X}" for v in values))
    return colors, explanation
