#!/usr/bin/env python3

import subprocess
import os
import glob
import sys
from typing import List


def _get_packages() -> List[str]:
    _PACKAGE_ENDING = 'nupkg'
    return list(glob.iglob(os.path.join('.', '**', f'*.{_PACKAGE_ENDING}')))


def _clean_packages():
    for package in _get_packages():
        os.remove(package)


def _build_packages():
    _CONFIGURATION = 'Release'
    subprocess.check_call(['dotnet', 'pack', '-c', _CONFIGURATION])


def _push_packages():
    _SOURCE = 'https://api.nuget.org/v3/index.json'
    _ENVVAR = 'NUGET_KEY'
    key = os.environ[_ENVVAR]
    if key is None:
        _ERROR_MSG = f'Error: The environment variable {_ENVVAR} has not been defined. Set its value to your NuGet API key. You can generate a key at https://www.nuget.org/account/apikeys'
        print(_ERROR_MSG, file=sys.stderr)
    for package in _get_packages():
        subprocess.check_call(['dotnet', 'nuget', 'push',
                               package, '-s', _SOURCE, '-k', key])


def push_all_packages():
    _clean_packages()
    _build_packages()
    _push_packages()


if __name__ == '__main__':
    push_all_packages()
