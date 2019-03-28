#!/usr/bin/env python3

import subprocess
import os
import glob
import sys
from typing import List

_CONFIGURATION = 'Release'


def _get_packages() -> List[str]:
    _PACKAGE_ENDING = 'nupkg'
    return list(glob.iglob(os.path.join('.', '**', 'bin', _CONFIGURATION, f'*.{_PACKAGE_ENDING}')))


def _clean_packages():
    for package in _get_packages():
        print(f'Removing old package at {package}')
        os.remove(package)


def _build_packages():
    subprocess.check_call(['dotnet', 'pack', '-c', _CONFIGURATION])


def _is_git_repo() -> bool:
    return os.path.isdir('.git')


def _get_git_branch() -> str:
    output = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    return output.decode('utf-8').strip()


def _is_on_master_branch() -> bool:
    return _get_git_branch() == 'master'


def _validate_environment():
    if _is_git_repo and not _is_on_master_branch():
        _ERROR_MSG = f'Error: Tried to push a NuGet package outside of the master branch (Current branch is {_get_git_branch()}). Merge your changes into master and rerun this script from there.'
        print(_ERROR_MSG, file=sys.stderr)
        exit(1)


def _push_packages():
    _SOURCE = 'https://api.nuget.org/v3/index.json'
    _ENVVAR = 'NUGET_KEY'
    key = os.environ[_ENVVAR]
    if key is None:
        _ERROR_MSG = f'Error: The environment variable {_ENVVAR} has not been defined. Set its value to your NuGet API key. You can generate a key at https://www.nuget.org/account/apikeys'
        print(_ERROR_MSG, file=sys.stderr)
        exit(1)
    for package in _get_packages():
        print(f'Pushing package at {package}')
        subprocess.check_call(['dotnet', 'nuget', 'push',
                               package, '-s', _SOURCE, '-k', key])


def push_all_packages():
    _validate_environment()

    _clean_packages()
    _build_packages()
    _push_packages()


if __name__ == '__main__':
    push_all_packages()
