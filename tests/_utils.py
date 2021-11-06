"""Test helpers."""

import contextlib
import os
import pathlib
import platform
import subprocess

__all__ = ['EXPECTED_DOT_BINARY', 'EXPECTED_DEFAULT_ENCODING',
           'as_cwd',
           'check_startupinfo', 'StartupinfoMatcher']

EXPECTED_DOT_BINARY = pathlib.Path('dot')

EXPECTED_DEFAULT_ENCODING = 'utf-8'


@contextlib.contextmanager
def as_cwd(path):
    """Return a context manager, which changes to the path's directory
        during the managed ``with`` context."""
    cwd = pathlib.Path().resolve()

    os.chdir(path)
    yield

    os.chdir(cwd)


def check_startupinfo(startupinfo) -> bool:  # noqa: N803
    return startupinfo is None


if platform.system().lower() == 'windows':
    def check_startupinfo(startupinfo) -> bool:  # noqa: N803,F811
        return (isinstance(startupinfo, subprocess.STARTUPINFO)
                and startupinfo.dwFlags & subprocess.STARTF_USESHOWWINDOW
                and startupinfo.wShowWindow == subprocess.SW_HIDE)


class StartupinfoMatcher:
    """Verify the given startupinfo argument is as expected for the plaform."""

    def __eq__(self, startupinfo) -> bool:
        return check_startupinfo(startupinfo)
