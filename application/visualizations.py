import sympy
import graphviz
import config
from datetime import datetime as dt


def get_truth_table(expression: str) -> tuple[list, list]:
    sympy_expr = sympy.sympify(expression, convert_xor=False)
    atoms = list(map(str, sympy_expr.atoms()))
    tt_gen = sympy.logic.boolalg.truth_table(
        sympy_expr, atoms
    )
    tt = [line for line in tt_gen]
    return (tt, atoms)


def draw_expression_tree(expression: str, view=True) -> str:
    dot_graph = sympy.dotprint(
        sympy.sympify(expression, convert_xor=False)
    )
    src = graphviz.Source(dot_graph)
    date_part = dt.now().strftime('%Y%m%d_%H%M%S')
    vis_filepath = (
        config.get('storage_loc') + f'expression_tree_{date_part}'
    )
    src.render(vis_filepath, view=view)
    return vis_filepath