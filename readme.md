# CLEA (Command-line Logic Expression Assessor)
## Introduction
A command line application that assists in simplifying, evaluating and visualising loigcal expressions for software developers. You can view the ongoing development process [here](https://cjduplessis.notion.site/Logician-Development-2380621b62534c5491a0f1a60282f342).

## Installation
```
git clone git@github.com:charljdp/clea.git
pip install -e ./application
```

## Python dependencies
- [Sympy](https://www.sympy.org/)
- [Graphviz](https://graphviz.readthedocs.io) (The Graphviz Python package)
- [Colorama](https://github.com/tartley/colorama)

## External dependencies
- [Graphviz](https://www.graphviz.org/) (The original Graphviz)

## Development
- [pipenv](https://pipenv.pypa.io/)
- [pytest](https://docs.pytest.org/)

## Unit testing
```
ENV=test && export ENV && pipenv run pytest
```