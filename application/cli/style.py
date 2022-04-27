import colorama, weakref
from functools import partial
from typing import Callable


_text_delimiters = {
    'logic_expression': '$',
    'frame': '#'
}

COLORTHEME_CHOICES = ['default', 'blue', 'dark']

#_contexts = ['help', 'error', 'normal']

class Style:
    def __init__(self, theme_name: str, lines_per_page: int):
        colorama.init()
        weakref.finalize(self, colorama.deinit)
        themes = {
            'default': DefaultTheme,
            'blue': BlueTheme,
            'dark': DarkTheme,
        }
        self._ColorTheme = themes[theme_name]
        self._margin_width = len(str(lines_per_page)) + 1

    def _colorful(self, string: str, context: str) -> str:
        ColorTheme = self._ColorTheme
        colorful_strings = []
        expr_delimiter = _text_delimiters['logic_expression']
        expr_text_list = string.split(expr_delimiter)
        # breakpoint()
        for i, substr in enumerate(expr_text_list):
            if substr == '':
                continue
            if i % 2 == 1:
                colorful_strings.append(
                    ColorTheme.by_delimiter(expr_delimiter)(substr)
                )
                continue
            frame_delimiter = _text_delimiters['frame']
            frame_text_list = substr.split(frame_delimiter)
            for j, subsubstr in enumerate(frame_text_list):
                if subsubstr == '':
                    continue
                if j % 2 == 1:
                    colorful_strings.append(
                        ColorTheme.by_delimiter(frame_delimiter)(subsubstr)
                    )
                    continue
                colorful_strings.append(
                    ColorTheme.by_context(context)(subsubstr)
                )
        return ''.join(colorful_strings)

    def apply(
        self, 
        margin: dict[str, str] = {}, 
        text: str = "", 
        context: str = 'normal'
    ) -> str:
        mtext = margin['text'] if margin != {} else ""
        mframe = margin['frame'] if margin != {} else ""
        mwidth = self._margin_width if margin != {} else 0
        
        space = " "*(mwidth - len(mtext))
        add_margin = lambda string: (
            f"{mtext}{space}{mframe} {string}"
            if margin != {}
            else string
        )
        if text == "":
            return self._colorful(
                add_margin(""), context
            )
        margined_text = [
            add_margin(s)
            for s in text.split("\n") 
            if s != ""
        ]
        return self._colorful(
            "\n".join(margined_text), 
            context
        )


# ======================= Colors =======================

def use_colors(fore="", back=""):
    '''
    Add colorama color to the text and/or background. 
    If color if not specified, then it assumed that bgcolor 
    is specified and vice versa.
    '''
    reset_sequence = ""
    if fore != "":
        reset_sequence = colorama.Fore.RESET
    if back != "":
        reset_sequence += colorama.Back.RESET

    return lambda text: (
        f"{back}{fore}{text}{reset_sequence}"
    )

# ======================== TEXT ==============================

WHITE = colorama.Fore.WHITE
CYAN = colorama.Fore.CYAN
LIGHTGREEN = colorama.Fore.LIGHTGREEN_EX
LIGHTYELLOW = colorama.Fore.LIGHTYELLOW_EX
LIGHTMAGENTA = colorama.Fore.LIGHTMAGENTA_EX
LIGHTCYAN = colorama.Fore.LIGHTCYAN_EX
BLACK = colorama.Fore.BLACK
BLUE = colorama.Fore.BLUE
GREEN = colorama.Fore.GREEN
GREY = colorama.Fore.LIGHTBLACK_EX
LIGHTBLUE = colorama.Fore.LIGHTBLUE_EX
LIGHTRED = colorama.Fore.LIGHTRED_EX
LIGHTWHITE = colorama.Fore.LIGHTWHITE_EX
MAGENTA = colorama.Fore.MAGENTA
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW

# ======================= BACKGROUND =============================

bgBLACK = colorama.Back.BLACK
bgBLUE = colorama.Back.BLUE
bgCYAN = colorama.Back.CYAN
bgYELLOW = colorama.Back.YELLOW
bgRED = colorama.Back.RED
bgWHITE = colorama.Back.WHITE

# bggrey = lambda text: colorama.Back.LIGHTBLACK_EX + text + reset_bgcolor
# bgwhite = lambda text: colorama.Back.WHITE + text + reset_bgcolor
# bgmagenta = lambda text: colorama.Back.MAGENTA + text + reset_bgcolor
# bgcyan = lambda text: colorama.Back.CYAN + text + reset_bgcolor
# bglightred = lambda text: colorama.Back.LIGHTRED_EX + text + reset_bgcolor
# bglightgreen = lambda text: colorama.Back.LIGHTGREEN_EX + text + reset_bgcolor
# bglightyellow = lambda text: colorama.Back.LIGHTYELLOW_EX + text + reset_bgcolor
# bglightblue = lambda text: colorama.Back.LIGHTBLUE_EX + text + reset_bgcolor
# bglightmagenta = lambda text: colorama.Back.LIGHTMAGENTA_EX + text + reset_bgcolor
# bglightcyan = lambda text: colorama.Back.LIGHTCYAN_EX + text + reset_bgcolor


def colorful_expression(expression: str, color_assignment: dict) -> str:
    colorful_expr = ''
    for char in expression:
        if char in ['&', '|', '^', '>', '<']:
            colorful_expr += color_assignment['operators'](char)
        elif char in ['(', ')']:
            colorful_expr += color_assignment['parentheses'](char)
        elif char.isalnum() or (char == '_'):
            colorful_expr += color_assignment['atoms'](char)
        elif (char == ' ') and ('space' in color_assignment):
            colorful_expr += color_assignment['space'](char)
        else:
            colorful_expr += char
    return colorful_expr


class DefaultTheme:
    def by_context(context: str) -> Callable[[str], str]:
        return {
            'help': use_colors(fore=GREEN),
            'error': use_colors(fore=LIGHTRED),
            'normal': use_colors(fore=LIGHTWHITE)
        }[context]

    def by_delimiter(symbol: str) -> Callable[[str], str]:
        return {
            '#': use_colors(fore=LIGHTBLUE),
            '$': partial(
                colorful_expression, 
                color_assignment={
                    'atoms': use_colors(fore=LIGHTWHITE),
                    'operators': use_colors(fore=GREY),
                    'parentheses': use_colors(fore=YELLOW)
                }
            )
        }[symbol]


class BlueTheme:
    def by_context(context: str) -> Callable[[str], str]:
        return {
            'help': use_colors(fore=LIGHTBLUE),
            'error': use_colors(fore=WHITE, back=bgCYAN),
            'normal': use_colors(fore=WHITE)
        }[context]

    def by_delimiter(symbol: str) -> Callable[[str], str]:
        return {
            '#': use_colors(fore=BLUE),
            '$': partial(
                colorful_expression, 
                color_assignment={
                    'atoms': use_colors(fore=CYAN),
                    'operators': use_colors(fore=LIGHTBLUE),
                    'parentheses': use_colors(fore=BLUE)
                }
            )
        }[symbol]


class DarkTheme:
    def by_context(context: str) -> Callable[[str], str]:
        return {
            'help': use_colors(fore=GREEN),
            'error': use_colors(fore=RED),
            'normal': use_colors(fore=GREY)
        }[context]

    def by_delimiter(symbol: str) -> Callable[[str], str]:
        return {
            '#': use_colors(fore=MAGENTA),
            '$': partial(
                colorful_expression, 
                color_assignment={
                    'atoms': use_colors(fore=MAGENTA),
                    'operators': use_colors(fore=BLUE),
                    'parentheses': use_colors(fore=GREY) 
                }
            )
        }[symbol]
