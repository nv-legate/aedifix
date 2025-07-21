# SPDX-FileCopyrightText: Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES.
#                         All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import sys

import pytest

from aedifix.packages.cuda import CudaArchAction, _guess_cuda_architecture

ARCH_STR: tuple[tuple[str, list[str]], ...] = (
    ("", []),
    (",,", []),
    ("70", ["70"]),
    ("70,80", ["70", "80"]),
    ("ampere", ["80"]),
    ("turing,hopper", ["75", "90"]),
    ("volta,60,all-major", ["70", "60", "all-major"]),
    ("60,,80", ["60", "80"]),
    ("50-real;120-real;121", ["50-real", "120-real", "121"]),
)


class TestCudaArchAction:
    @pytest.mark.parametrize(("argv", "expected"), ARCH_STR)
    def test_map_cuda_arch_names(self, argv: str, expected: list[str]) -> None:
        ret = CudaArchAction.map_cuda_arch_names(argv)
        assert ret == expected


class TestCUDA:
    @pytest.mark.parametrize(
        ("env_var", "env_value", "expected"),
        [
            ("CUDAARCHS", "volta", "volta"),
            ("CUDAARCHS", "volta;ampere", "volta;ampere"),
            ("CMAKE_CUDA_ARCHITECTURES", "75", "75"),
            ("", "", "all-major"),
        ],
    )
    def test_default_cuda_arches(
        self,
        monkeypatch: pytest.MonkeyPatch,
        env_var: str,
        env_value: str,
        expected: str,
    ) -> None:
        if env_var:
            monkeypatch.setenv(env_var, env_value)

        assert _guess_cuda_architecture() == expected


if __name__ == "__main__":
    sys.exit(pytest.main())
