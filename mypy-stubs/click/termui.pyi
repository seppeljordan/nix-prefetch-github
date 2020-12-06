from typing import Any, Optional

from ._compat import DEFAULT_COLUMNS as DEFAULT_COLUMNS
from ._compat import WIN as WIN
from ._compat import get_winterm_size as get_winterm_size
from ._compat import isatty as isatty
from ._compat import raw_input as raw_input
from ._compat import string_types as string_types
from ._compat import strip_ansi as strip_ansi
from ._compat import text_type as text_type
from .exceptions import Abort as Abort
from .exceptions import UsageError as UsageError
from .globals import resolve_color_default as resolve_color_default
from .types import Choice as Choice
from .types import Path as Path
from .types import convert_type as convert_type
from .utils import LazyFile as LazyFile
from .utils import echo as echo

visible_prompt_func = raw_input

def hidden_prompt_func(prompt: Any): ...
def prompt(
    text: Any,
    default: Optional[Any] = ...,
    hide_input: bool = ...,
    confirmation_prompt: bool = ...,
    type: Optional[Any] = ...,
    value_proc: Optional[Any] = ...,
    prompt_suffix: str = ...,
    show_default: bool = ...,
    err: bool = ...,
    show_choices: bool = ...,
): ...
def confirm(
    text: Any,
    default: bool = ...,
    abort: bool = ...,
    prompt_suffix: str = ...,
    show_default: bool = ...,
    err: bool = ...,
): ...
def get_terminal_size(): ...
def echo_via_pager(text_or_generator: Any, color: Optional[Any] = ...): ...
def progressbar(
    iterable: Optional[Any] = ...,
    length: Optional[Any] = ...,
    label: Optional[Any] = ...,
    show_eta: bool = ...,
    show_percent: Optional[Any] = ...,
    show_pos: bool = ...,
    item_show_func: Optional[Any] = ...,
    fill_char: str = ...,
    empty_char: str = ...,
    bar_template: str = ...,
    info_sep: str = ...,
    width: int = ...,
    file: Optional[Any] = ...,
    color: Optional[Any] = ...,
): ...
def clear() -> None: ...
def style(
    text: Any,
    fg: Optional[Any] = ...,
    bg: Optional[Any] = ...,
    bold: Optional[Any] = ...,
    dim: Optional[Any] = ...,
    underline: Optional[Any] = ...,
    blink: Optional[Any] = ...,
    reverse: Optional[Any] = ...,
    reset: bool = ...,
): ...
def unstyle(text: Any): ...
def secho(
    message: Optional[Any] = ...,
    file: Optional[Any] = ...,
    nl: bool = ...,
    err: bool = ...,
    color: Optional[Any] = ...,
    **styles: Any
): ...
def edit(
    text: Optional[Any] = ...,
    editor: Optional[Any] = ...,
    env: Optional[Any] = ...,
    require_save: bool = ...,
    extension: str = ...,
    filename: Optional[Any] = ...,
): ...
def launch(url: Any, wait: bool = ..., locate: bool = ...): ...
def getchar(echo: bool = ...): ...
def raw_terminal(): ...
def pause(info: str = ..., err: bool = ...) -> None: ...
