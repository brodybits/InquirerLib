# QUICK WORKAROUND - EXPECTED ISSUE ON WINDOWS

from prompt_toolkit.input.posix_pipe import _Pipe, PosixPipeInput


def get_pipe_input():
    return PosixPipeInput(_Pipe())
