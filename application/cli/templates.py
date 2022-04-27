"""
All output templates are here.
"""

ABOUT = f"""
#{'-'*100}#
#|#{' '*38}A B O U T    C L E A{' '*38}#|#
#{'-'*100}#
Command-line Logic Expression Assessor (CLEA) assists you in reasoning about logical expressions or 
formulas. The operators that are supported are:
    
    &: and
    |: or
    ^: exclusive-or
    ~: not

"""


HELP = f"""
    #{'-'*52}#
    #|#   CLEA (Command-line Logic Expression Assessor   #|#
    #{'-'*52}#

    operation logic_expression
    operation is one of,
        anf    - Algebraic Normal Form
        cnf    - Conjunctive Normal Form
        dnf    - Disjunctive Normal Form
        nnf    - Negation Normal Form
        nf     - All normal forms
        sim    - Simplify expression
        sum    - Summary of expression. Includes
        ei     - Eliminate implications
        all    - Do everything
        tree   - Draw an expression tree
        table  - Draw a truth table
        models - If the expression is satisfiable, a list of models is printed.

    map logic_expression1, logic_expression2
        Computes a mapping between the atoms of logic_expression1 and logic_expression2, if there is such a mapping.

    help    - Prints help
    exit    - Exit the application
"""

def normal_forms(normal_form_dict: dict) -> str:
    if len(normal_form_dict) == 1:
        expr = list(normal_form_dict.values())[0]
        return f"${expr}$"
    
    return "\n".join(
        [
            f" {form}: ${expression}$" 
            for form, expression 
            in normal_form_dict.items()
        ]
    )


def summary(
    logic_expression,
    symplified,
    normal_form_dict,
    models
) -> str:
    normal_forms = [
        f"{form}: ${expression}$\n" 
        for form, expression 
        in normal_form_dict.items()
    ]

    models_temp = [
        f"{model}\n" 
        for model 
        in models
    ]

    raw_template = [
        f"SUMMARY: ${logic_expression}$\n",
        f"#{'-'*52}#\n",
        f"Simplified: ${symplified}$\n",
        "Normal forms\n",
        f"#{'-'*12}#\n",
        *normal_forms,
        "Models\n",
        f"#{'-'*12}#\n",
        *models_temp
    ]
    return ''.join(raw_template) 


def atom_mapping(mapping: dict) -> str:
    if mapping == {}:
        return "No mapping is possible."
        
    return "\n".join(
        f"${atom}$  ->  ${mapped_atom}$" 
        for atom, mapped_atom 
        in mapping.items()
    )


def truth_table(truth_table_values: list, atoms: str) -> str:
    # heading
    tt = "  ".join([f"${atom}$" for atom in atoms]) + " #|# $F$\n"
    tt += f"#{'-'*len(tt)}#\n"
    for invals, outval in truth_table_values:
        tt += "  ".join(list(map(str, invals)))
        tt += " #|# " + str(int(bool(outval))) + "\n"
    return tt
