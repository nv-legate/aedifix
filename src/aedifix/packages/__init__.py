# SPDX-FileCopyrightText: Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES.
#                         All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..package.package import Package


from .cmake import CMake
from .cuda import CUDA
from .python import Python


def _all_default_packages() -> list[type[Package]]:
    return [CMake, CUDA, Python]


__all__ = ("CUDA", "CMake", "Python")
