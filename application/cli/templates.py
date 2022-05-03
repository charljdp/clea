"""
All output templates are here.
"""

ABOUT = f"""
#{'-'*100}#
#|#{' '*39}A B O U T    C L E A{' '*39}#|#
#{'-'*100}#
Command-line Logic Expression Assessor (CLEA) assists you in reasoning about (Boolean) logical expressions or 
formulas.
    Examples: 
      A & B & (C | D)
      X ^ (Y & ~Z)

The operators that are supported are:

    &: and
    |: or
    ^: exclusive-or
    ~: not
    
Variable assignment:

    <variable_name> = <logic expression>
    
    The variable assignment is equivalent to a definition assignment. 
    It holds the unevaluated logic expression.

    Variable names may only contain letters, numbers and underscores but may not start with a number.

Uasge:

    1  | A = X & Y & (X ^ Z)
    2  | cnf A

         X & Y & (X | Z) & (~X | ~Z)
    
    3  | table ~X | ~Z
    
        Z  X | F
        --------
        0  0 | 1
        0  1 | 1
        1  0 | 1
        1  1 | 0
"""


HELP = f"""
    Each command consists of an operation and one or two logical expressions 
    depending on the operation.

    Operations with the syntax: <operation> <expression>
        anf     Algebraic Normal Form
        cnf     Conjunctive Normal Form
        dnf     Disjunctive Normal Form
        nnf     Negation Normal Form
        nf      All normal forms
        sim     Simplify expression
        sum     Summary of expression
        ei      Eliminate implications
        tree    Draw an expression tree
        table   Draw a truth table
        models  If the expression is satisfiable, a list of models is printed.
    
    Operations with the syntax: <operation> <expression_1>, <expression_2>
        map     Computes a mapping between the atoms of expression_1 and expression_2, 
                if there is such a mapping.

    Other commands:
        help    Prints help
        exit    Exit the application
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
