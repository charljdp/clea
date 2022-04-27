import pytest
from logic import (
    LogicExpressionCollection, 
    CircularRefernceError
)


@pytest.mark.logic
def test_invalid_expressions():
    coll_obj = LogicExpressionCollection()
    with pytest.raises(Exception):
        coll_obj.add('_1', '')
    with pytest.raises(Exception):
        coll_obj.add('_2', 'A & (B')
    with pytest.raises(CircularRefernceError):
        coll_obj.add('A', 'A & B')
    with pytest.raises(CircularRefernceError):
        coll_obj.add('A', 'B | C')
        coll_obj.add('X', 'A ^ B')
        coll_obj.add('C', 'X & Y')


@pytest.mark.logic
def test_names():
    coll_obj = LogicExpressionCollection()
    invalid_var_names = [
        'true', 
        'false',
        '2',
        '1A',
        'E A',
        '#'
    ]
    for name in invalid_var_names:
        assert coll_obj.add(name, 'A & B') > ""
    


@pytest.mark.logic
def test_simplify(simplifiable_logic):
    coll_obj = LogicExpressionCollection()
    assert (
        coll_obj.simplify(simplifiable_logic['expression']) 
        in simplifiable_logic['simplified']
    )


@pytest.mark.logic
def test_eliminate_implications(implication_logic, boolean_operator):
    coll_obj = LogicExpressionCollection()
    le_no_implications = coll_obj.eliminate_implications(implication_logic)
    assert le_no_implications.find(boolean_operator['IMPLIES']) == -1
    assert le_no_implications.find(boolean_operator['OR']) != -1
    assert le_no_implications.find(boolean_operator['NOT']) != -1


@pytest.mark.logic
def test_get_models(some_logic, unsatisfiable_logic, single_tautology_logic):
    # A logical expression that only has one model that is always true
    coll_obj = LogicExpressionCollection()
    coll_obj.add('L1', single_tautology_logic)
    coll_obj.add('L2', some_logic['expression'])
    coll_obj.add('L3', unsatisfiable_logic)
    assert coll_obj.get_models('L1') == [{'True': True}]

    # Some satisfiable logic returns models
    for model in coll_obj.get_models('L2'):
        assert model['A'] or (model['C'] and model['B'])

    # Unsatisfiable logic returns no models, i.e. an empty list
    assert coll_obj.get_models('L3') == []


@pytest.mark.logic
def test_to_normal_form(some_logic):
    coll_obj = LogicExpressionCollection()
    all_normal_forms = list(coll_obj.to_normal_form(some_logic['expression']).keys())
    all_normal_forms.sort()
    assert all_normal_forms == ['anf', 'cnf', 'dnf', 'nnf']
    for option in all_normal_forms:
        assert (
            coll_obj.to_normal_form(some_logic['expression'], options=[option])[option] 
            == some_logic[option]
        )
