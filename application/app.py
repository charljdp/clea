'''
The entry point for Logician.
'''

from cli.cli import CLI
from cli import templates
import logic
import visualizations as vis

# TODO: import modules as "import x as _x"
# TODO: Organise modules' functions and variables
def main():
    '''
    The app entry point.
    '''
    cli = CLI()
    cli.prints(templates.ABOUT, margined=False)
    le_coll_obj = logic.LogicExpressionCollection()
    for command in cli.commands():
        try:
            operation = command[0]
            arguments = command[1]
            if operation == 'assign':
                error_msg = le_coll_obj.add(arguments[0], arguments[1])
                if error_msg > "":
                    cli.prints(error_msg)
            if operation == 'del':
                if le_coll_obj.delete(arguments[0]):
                    cli.prints(f'Variable ${arguments[0]}$ deleted.')
                else:
                    cli.prints(
                        f'Variable ${arguments[0]}$ does not exist.', 
                        context='error'
                    )
            if operation in ['anf', 'cnf', 'dnf', 'nnf', 'nf']:
                if operation == 'nf':
                    nf = le_coll_obj.to_normal_form(arguments[0])
                else:
                    nf = le_coll_obj.to_normal_form(arguments[0], [operation])
                cli.prints(templates.normal_forms(nf))
            if operation == 'sim':
                cli.prints(le_coll_obj.simplify(arguments[0]))
            if operation == 'ei':
                cli.prints(
                    le_coll_obj.eliminate_implications(arguments[0])
                )
            if operation == 'map':
                map = le_coll_obj.get_equivalence_map(arguments[0], arguments[1])
                cli.prints(templates.atom_mapping(map))
            if operation == 'sum':
                cli.prints(
                    templates.summary(
                        le_coll_obj.simplify(arguments[0]),
                        le_coll_obj.to_normal_form(arguments[0], options=['cnf', 'dnf']),
                        le_coll_obj.get_models(arguments[0])
                    )
                )
            if operation == 'table':
                cli.prints(
                    templates.truth_table(
                        *vis.get_truth_table(arguments[0])
                    )
                )
            if operation == 'tree':
                cli.prints(f"Rendering expression tree for ${arguments[0]}$ ...")
                vis.draw_expression_tree(arguments[0])
        except Exception as error:
            cli.prints(str(error), context='error')
