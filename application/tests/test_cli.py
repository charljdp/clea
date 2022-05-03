import pytest
from cli.cli import CLI
from cli.style import DefaultTheme, DarkTheme
import config
from colorama import Back, Fore

def create_mock_input(inputs):
    it = iter(inputs)
    return lambda: next(it)


@pytest.mark.cli
def test_cli_default_args(monkeypatch):
    config.reset()
    with monkeypatch.context() as mp:
        mp.setattr('sys.argv', ['clea'])
        cli_obj = CLI()
        assert cli_obj._Style._ColorTheme is DefaultTheme
        assert cli_obj._lines_per_page == 10


@pytest.mark.cli
def test_cli_nondefault_args(monkeypatch):
    config.reset()
    with monkeypatch.context() as mp:
        args = ['clea', '-t', 'dark', '-n', '12']
        mp.setattr('sys.argv', args)
        cli_obj = CLI()
        assert cli_obj._Style._ColorTheme is DarkTheme
        assert cli_obj._lines_per_page == 12


@pytest.mark.cli
def test_cli_erroneous_arg(monkeypatch):
    config.reset()
    with monkeypatch.context() as mp:
        mp.setattr('sys.argv', ['clea', '-s', 'c:\some_non_existent_location'])
        with pytest.raises(SystemExit):
            cli_obj = CLI()
        mp.setattr('sys.argv', ['clea', '-n', '0'])
        with pytest.raises(SystemExit):
            cli_obj = CLI()


@pytest.mark.cli
def test_prints(monkeypatch, capsys):
    with monkeypatch.context() as mp:
        mp.setattr('sys.argv', ['clea', '-t', 'dark'])
        cli = CLI()
        cli.prints('abc', context='normal')
        printed = capsys.readouterr().out
        assert ':' in printed
        cli.prints('abc', context='normal', margined=False)
        printed = capsys.readouterr().out
        assert ':' not in printed


@pytest.mark.cli
def test_commands(monkeypatch):
    mock_commands = [
        'X = A & B | C',
        'dnf A & B',
        'cnf E & (D >> A)',
        'exit'
    ]
    mock_input = create_mock_input(mock_commands)
    config.reset()
    with monkeypatch.context() as mp:
        mp.setattr('sys.argv', ['clea'])
        cli = CLI()
        cli._input = lambda _: mock_input() 
        for index, command in enumerate(cli.commands()):
            if index == 0:
                assert command == ('assign', ['X', 'A & B | C'])
            if index == 1:
                assert command == ('dnf', ['A & B', None])
            if index == 2:
                assert command == ('cnf', ['E & (D >> A)', None])
        