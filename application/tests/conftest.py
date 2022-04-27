import pytest
import os

@pytest.fixture
def test_dir():
    temp_dir = r'.\test_dir'
    os.mkdir(temp_dir)
    yield temp_dir
    os.rmdir(temp_dir)


@pytest.fixture
def boolean_operator():
    return {
        'AND': '&',
        'OR': '|',
        'IMPLIES': '>>',
        'NOT': '~'
    }


@pytest.fixture
def single_tautology_logic():
    return 'True & True'


@pytest.fixture
def some_logic():
    return {
        'expression': 'A | (C & B)',
        'anf': 'A ^ (B & C) ^ (A & B & C)',
        'cnf': '(A | B) & (A | C)',
        'dnf': 'A | (B & C)',
        'nnf': 'A | (B & C)'
    }


@pytest.fixture
def unsatisfiable_logic():
    return 'A & ~A'


@pytest.fixture
def tautology_logic():
    return 'A | ~A'


@pytest.fixture
def implication_logic():
    return 'A >> B'


@pytest.fixture
def equivalence_logic():
    return '(A >> B) & (B >> A)'


@pytest.fixture
def simplifiable_logic():
    return {
        'expression': 'A & A & B',
        'simplified': ('A & B', 'B & A')
    }
