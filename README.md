# aedifix

# Bootstrapping aedifix in your build

Assuming your main package is called `MyMainPacakge` and lives in `my_main_package.py`,
you may use the following snippet to create a `configure` script that automatically
bootstraps `aedifix` on first call.

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys


def ensure_aedifix() -> None:
    r"""Ensure aedifix is bootstrapped."""
    from importlib.metadata import PackageNotFoundError, version

    from packaging.version import Version

    VERSION = Version("1.2.0")

    try:
        mod_version = Version(version("aedifix"))

        if mod_version == VERSION:
            return

        if mod_version.is_devrelease:
            # If its a "dev release" that means it's editable installed,
            # meaning someone is working on aedifix. We don't care that the
            # versions don't match in this case.
            return

        raise RuntimeError  # noqa: TRY301
    except (PackageNotFoundError, RuntimeError):
        from subprocess import check_call

        package = f"git+https://github.com/nv-legate/aedifix@{VERSION}"
        check_call([sys.executable, "-m", "pip", "install", package])


ensure_aedifix()

from my_main_package import MyMainPackage  # noqa: E402

from aedifix.main import basic_configure  # noqa: E402


def main() -> int:
    r"""Run configure.

    Returns
    -------
    int
        An integer error code, or 0 on success.
    """
    return basic_configure(tuple(sys.argv[1:]), MyMainPackage)


if __name__ == "__main__":
    sys.exit(main())

```
