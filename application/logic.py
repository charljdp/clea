'''
TODO: Make sure about method parameter types and return types.
'''
import sympy as _sympy
import re


_valid_var_name_re = re.compile(r'^[a-zA-Z_]+\w*$')


class CircularRefernceError(Exception):
    pass


class LogicExpressionCollection:

    def __init__(self):
        self._variables = {}

    def _is_referenced(self, var_name: str, expr: str) -> bool:
        chars = '[&\s\)\(\|\^)]'
        matches = re.findall(
            rf'(?<=^){var_name}(?={chars})|' + 
            rf'(?<={chars}){var_name}(?={chars})|' +
            rf'(?<=^){var_name}(?=$)|' +
            rf'(?<={chars}){var_name}(?=$)',  
            expr
        )
        return len(matches) > 0

    def _sympified(self, expression: str):
        return _sympy.sympify(
            expression, 
            convert_xor=False
        )

    def _substitute_vars(self, expr):
        expr_substituted = expr
        for var in self._variables:
            if not self._is_referenced(var, expr_substituted):
                continue
            str_list_without_var = expr_substituted.split(var)
            s = f'({self._variables[var]})'
            expr_substituted = s.join(str_list_without_var)
        if expr != expr_substituted:
            self._substitute_vars(expr_substituted)
        return expr_substituted

    def _check_circular_referencing(self, var_name, expr, prev_var_name=''):
        if self._is_referenced(var_name, expr):
            assignment = f"{prev_var_name} = {expr}"
            user_reference = (
                f" See assignment {assignment}." 
                if prev_var_name != "" 
                else ""
            )
            raise CircularRefernceError(
                f"Cannot assign a variable to itself.{user_reference}"
            )
        for prev_var_name in self._variables:
            if not self._is_referenced(prev_var_name, expr): continue
            self._check_circular_referencing(
                var_name, 
                self._variables[prev_var_name], 
                prev_var_name
            )

    def add(self, var_name, expression):
        # Check if expression is valid.
        self._sympified(expression)
        # Check if a variable appears on 
        # both sides of the equal symbol
        self._check_circular_referencing(
            var_name, 
            expression
        )
        if var_name.lower() in ['true', 'false']:
            return (
                "Cannot use True and False as variables. " +
                "They are reserved for logical true and logical " +
                "false respectively."
            )
        if not _valid_var_name_re.match(var_name):
            return "Invalid variable name."
        self._variables[var_name] = expression
        return ""

    def delete(self, var_name):
        if var_name not in self._variables:
            return False
        del self._variables[var_name]
        return True
    
    def simplify(self, expression, **options):
        expr = self._substitute_vars(expression)
        return str(_sympy.logic.boolalg.simplify_logic(
            self._sympified(expr)
        ))

    def to_normal_form(self, expression, options: list[str] = []) -> dict:
        result = {}
        if options == []:
            options = ['anf', 'cnf', 'dnf', 'nnf']
        expr = self._substitute_vars(expression)
        sympy_expr = self._sympified(expr)
        if 'anf' in options:
            result['anf'] = str(_sympy.logic.boolalg.to_anf(sympy_expr))
        if 'cnf' in options:
            result['cnf'] = str(_sympy.logic.boolalg.to_cnf(sympy_expr))
        if 'dnf' in options:
            result['dnf'] = str(_sympy.logic.boolalg.to_dnf(sympy_expr))
        if 'nnf' in options:
            result['nnf'] = str(_sympy.logic.boolalg.to_nnf(sympy_expr))
        return result

    def eliminate_implications(self, expression: str) -> str:
        expr = self._substitute_vars(expression)
        return str(
            _sympy.logic.boolalg.eliminate_implications(
                self._sympified(expr)
            )
        )

    def get_models(self, expression: str):
        expr = self._substitute_vars(expression)
        models = _sympy.logic.inference.satisfiable(
            self._sympified(expr),
            all_models=True
        )  # Generator is returned
        model_list = []
        for model in models:
            if model:
                model_dict = {}
                for key, value in model.items():
                    model_dict[str(key)] = bool(value)
                model_list.append(model_dict)
            else:
                # If logical expression is 
                # unsatisfiable then model = False
                return []
        return model_list

    def get_equivalence_map(self, expr1, expr2) -> dict:

        '''
        Computes a mapping of atoms between the given expressions.
        Currently limited to two logical expressions.
        
        Parameters
        ----------
        expr_list: list of LogicExpression objects

        Returns
        -------
        The mapping of the atoms in the form of a dict.
        '''
        expr1_sub = self._sympified(self._substitute_vars(expr1))
        expr2_sub = self._sympified(self._substitute_vars(expr2))
        mapping = _sympy.logic.boolalg.bool_map(expr1_sub, expr2_sub)

        if not mapping:
            return {}

        return mapping[1]