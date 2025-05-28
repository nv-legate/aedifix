# SPDX-FileCopyrightText: Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES.
#                         All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Final

from ..package import Package
from ..util.argument_parser import ArgSpec, ConfigArgument

if TYPE_CHECKING:
    from ..manager import ConfigurationManager


class Python(Package):
    name = "Python"

    With_Python: Final = ConfigArgument(
        name="--with-python",
        spec=ArgSpec(
            dest="with_python", type=bool, help="Build with Python bindings."
        ),
        enables_package=True,
        primary=True,
    )

    def summarize(self) -> str:
        r"""Summarize configured Python.

        Returns
        -------
        summary : str
            The summary of Python.
        """
        return self.create_package_summary(
            [("Executable", sys.executable), ("Version", sys.version)]
        )


def create_package(manager: ConfigurationManager) -> Python:
    return Python(manager)
