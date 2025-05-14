# SPDX-FileCopyrightText: Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES.B
#                         All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from os import environ
from pathlib import Path
from typing import TYPE_CHECKING

from .dummy_main_package import DummyMainPackage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from aedifix.manager import ConfigurationManager


class DummyMainModule(DummyMainPackage):
    name = "DummyMainModule"

    def __init__(
        self, manager: ConfigurationManager, argv: Sequence[str]
    ) -> None:
        super().__init__(
            manager=manager,
            argv=argv,
            arch_name="AEDIFIX_PYTEST_ARCH",
            project_dir_name="AEDIFIX_PYTEST_DIR",
            project_dir_value=Path(environ["AEDIFIX_PYTEST_DIR"]),
        )

    @classmethod
    def from_argv(
        cls, manager: ConfigurationManager, argv: Sequence[str]
    ) -> DummyMainModule:
        return cls(manager, argv)
