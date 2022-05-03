'''
cli.py impli
'''
import argparse
import os, re
import config
from cli.templates import HELP
from cli.style import Style, COLORTHEME_CHOICES


class CLI:
    def __init__(self):
        args = _parse_args()
        for arg in args:
            if args[arg] is None:
                args[arg] = config.get(arg)
        config.set(args)
        self._lines_per_page = config.get('lines_per_page')
        self._Style = Style(config.get('theme'), self._lines_per_page)

    def commands(self):
        line_no = 0
        page_no = 0
        while True:
            if (line_no % self._lines_per_page) == 0:
                line_no = 0
                page_no += 1
                self.prints(
                    f"#{'-'*20}# PAGE {page_no} #{'-'*20}#",
                    margined=False
                )
            line_no += 1
            next_command = self._input(
                self._Style.apply(
                    margin={'text': str(line_no), 'frame': '#|#'}
                )
            )
            if _is_exit_signal(next_command):
                break
            if _is_help_signal(next_command):
                self.prints(HELP, 'help')
                continue
            try:
                parse_result = _parse_command(next_command)
                yield parse_result
            except Exception as e:
                self.prints(str(e))

    def _input(self, prompt):
        try:
            print(prompt, end="")
            return input()
        finally:
            print()

    def prints(
        self, 
        text: str, 
        context: str = 'normal', 
        margined: bool = True
    ) -> None:
        ''' Prints the text to the command line interface.
            Parameters:
                text: str
                context: str (default: 'normal') 
                    possible values: 'normal', 'help' and 'error'
        '''
        # breakpoint()
        margin = {'text': "", 'frame': "#:#"} if margined else {}
        styled_text = self._Style.apply(
            margin=margin,
            text=text, 
            context=context
        )
        print(styled_text, "\n")


class CheckIntGreaterThanZero(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 1:
            parser.error(
                f"The value for argument {option_string} " +
                "must be greater than 0."
            )
        setattr(namespace, self.dest, values)


class CheckDirectoryPath(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.exists(values[0]):
            parser.error(
                f"Path {values} specified for option {option_string} " +
                "is not a directory or it does not exist.\n"
            )
        setattr(namespace, self.dest, values)


def _parse_args() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        choices=COLORTHEME_CHOICES,
        default=argparse.SUPPRESS,
        help="Choose a color theme for the prints."
    )
    parser.add_argument(
        '-s',
        default=argparse.SUPPRESS,
        action=CheckDirectoryPath,
        help="Specifiy a location where to save any out files."
    )
    parser.add_argument(
        '-n',
        type=int,
        default=argparse.SUPPRESS,
        action=CheckIntGreaterThanZero,
        help="The number of lines per page. Must be greater than 0."
    )
    options = vars(parser.parse_args())
    return {
        'theme': options.get('t'),
        'storage_loc': options.get('s'),
        'lines_per_page': options.get('n')
    }


valid_operations = [
    'map', 'del', 'ei', 
    'nf', 'anf', 'cnf', 
    'dnf', 'nnf', 'sim', 
    'sum', 'tree',
    'table', 'models'
]


valid_operation_re = re.compile(
    r'|'.join([
        rf'(?<=^){oper}(?=\s)|(?<=\s){oper}(?=\s)|(?<=\s){oper}(?=$)' 
        for oper in valid_operations
    ])
)


def _is_exit_signal(text: str) -> bool:
    return text.lower() == 'exit'


def _is_help_signal(text: str) -> bool:
    return text.lower() == 'help'


class SyntaxErrorCLI(Exception):
    pass


def _parse_command(command: str) -> tuple[str]:
    # TODO: Sort out this function
    pos = command.find('=')
    error_msg = ""
    if pos > -1:
        var_part, expr_part = command.split('=')
        var_part = var_part.strip()
        expr_part = expr_part.strip()
        return ('assign', [var_part, expr_part])
    else:
        found_list = valid_operation_re.findall(command)
        if len(found_list) == 1:
            keyword = found_list[0]
            start_of_args = command.find(keyword) + len(keyword)
            if keyword == 'map':
                comma_pos = command.find(',', start_of_args)
                if comma_pos == -1:
                    error_msg = ''
                else:
                    arg1 = command[start_of_args:comma_pos].strip()
                    arg2 = command[comma_pos + 1:].strip()
                    return ('map', [arg1, arg2])
            else:
                arg = command[start_of_args:].strip()
                return (keyword, [arg, None])
        if len(found_list) == 0:
            error_msg = 'No operation specified.'
        if len(found_list) > 1:
            error_msg = 'Too many operations specified.'
    raise SyntaxErrorCLI(error_msg)
