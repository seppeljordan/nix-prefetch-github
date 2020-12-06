import ctypes
import io
from ctypes import WinError as WinError
from typing import Any

from ._compat import PY2 as PY2
from ._compat import text_type as text_type

PyObject_GetBuffer: Any
PyBuffer_Release: Any
c_ssize_p: Any
kernel32: Any
GetStdHandle: Any
ReadConsoleW: Any
WriteConsoleW: Any
GetConsoleMode: Any
GetLastError: Any
GetCommandLineW: Any
CommandLineToArgvW: Any
LocalFree: Any
STDIN_HANDLE: Any
STDOUT_HANDLE: Any
STDERR_HANDLE: Any
PyBUF_SIMPLE: int
PyBUF_WRITABLE: int
ERROR_SUCCESS: int
ERROR_NOT_ENOUGH_MEMORY: int
ERROR_OPERATION_ABORTED: int
STDIN_FILENO: int
STDOUT_FILENO: int
STDERR_FILENO: int
EOF: bytes
MAX_BYTES_WRITTEN: int

class Py_buffer(ctypes.Structure): ...

get_buffer: Any

class _WindowsConsoleRawIOBase(io.RawIOBase):
    handle: Any = ...
    def __init__(self, handle: Any) -> None: ...
    def isatty(self): ...

class _WindowsConsoleReader(_WindowsConsoleRawIOBase):
    def readable(self): ...
    def readinto(self, b: Any): ...

class _WindowsConsoleWriter(_WindowsConsoleRawIOBase):
    def writable(self): ...
    def write(self, b: Any): ...

class ConsoleStream:
    buffer: Any = ...
    def __init__(self, text_stream: Any, byte_stream: Any) -> None: ...
    @property
    def name(self): ...
    def write(self, x: Any): ...
    def writelines(self, lines: Any) -> None: ...
    def __getattr__(self, name: Any): ...
    def isatty(self): ...

class WindowsChunkedWriter:
    def __init__(self, wrapped: Any) -> None: ...
    def __getattr__(self, name: Any): ...
    def write(self, text: Any) -> None: ...
