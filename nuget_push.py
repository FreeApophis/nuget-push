#!/usr/bin/env python3

import subprocess
import os
import glob
from typing import List

_PACKAGE_ENDING = "nupkg"


def _get_packages() -> List[str]:
    return list(glob.iglob(os.path.join(".", "**", f'*.{_PACKAGE_ENDING}')))


def _clean_packages():
    for package in _get_packages():
        os.remove(package)


def _build_packages():
    _CONFIGURATION = "Release"
    subprocess.check_call(["dotnet", "pack", "-c", _CONFIGURATION])


def _push_packages():
    _SOURCE = "https://api.nuget.org/v3/index.json"
    _ENVVAR = "NUGET_KEY"
    key = os.environ[_ENVVAR]
    for package in _get_packages():
        subprocess.check_call(["dotnet", "nuget", "push",
                               package, "-s", _SOURCE, "-k", key])


def push_all_packages():
    _clean_packages()
    _build_packages()
    _push_packages()


if __name__ == '__main__':
    push_all_packages()
