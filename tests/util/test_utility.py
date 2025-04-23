# SPDX-FileCopyrightText: Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES.
#                         All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import sys

import pytest

from aedifix.util.utility import (
    deduplicate_command_line_args,
    dest_to_flag,
    flag_to_dest,
    partition_argv,
    prune_command_line_args,
)


class TestUtility:
    def test_prune_command_line_args_empty(self) -> None:
        argv = [
            "--foo",
            "--bar=1",
            "--baz",
            "0",
            "1",
            "asdasd",
            "--remain",
            "--foo=yes",
            "--bar",
            "1",
        ]

        new_argv = prune_command_line_args(argv, set())
        assert new_argv == argv

    def test_prune_command_line_args(self) -> None:
        to_remove = {"--foo", "--bar", "--baz"}
        argv = [
            "--foo",
            "--bar=1",
            "--baz",
            "0",
            "1",
            "asdasd",
            "--remain",
            "--foo=yes",
            "--bar",
            "1",
        ]

        new_argv = prune_command_line_args(argv, to_remove)
        assert new_argv == ["--remain"]

    def test_prune_command_line_args_bad(self) -> None:
        bad_remove = {"asdasd", "asdau999"}

        with pytest.raises(
            ValueError, match=r"Argument '.*' must start with '-'"
        ):
            prune_command_line_args([], bad_remove)

    def test_deduplicate_command_line_args(self) -> None:
        argv = [
            "--foo=1",
            "--foo",
            "--foo=45",
            "--hello",
            "world",
            "--foo",
            "2",
            "--bar",
            "--baz=17",
        ]
        new_argv = deduplicate_command_line_args(argv)
        assert new_argv == [
            "--foo",
            "2",
            "--hello",
            "world",
            "--bar",
            "--baz=17",
        ]

    def test_deduplicate_command_line_args_empty(self) -> None:
        new_argv = deduplicate_command_line_args([])
        assert new_argv == []

    def test_deduplicate_command_line_args_positional_arg(self) -> None:
        new_argv = deduplicate_command_line_args(["foo", "--bar", "--foo"])
        assert new_argv == ["foo", "--bar", "--foo"]

    @pytest.mark.parametrize(
        ("flag_str", "expected"),
        (("", ""), ("--foo", "foo"), ("-f", "f"), ("-foo--bar", "foo__bar")),
    )
    def test_flag_to_dest(self, flag_str: str, expected: str) -> None:
        assert flag_to_dest(flag_str) == expected

    @pytest.mark.parametrize(
        ("dest_str", "expected"),
        (
            ("", "--"),
            ("foo", "--foo"),
            ("f", "--f"),
            ("foo_bar", "--foo-bar"),
            ("foo-bar", "--foo-bar"),
        ),
    )
    def test_dest_to_flag(self, dest_str: str, expected: str) -> None:
        assert dest_to_flag(dest_str) == expected

    @pytest.mark.parametrize(
        ("argv", "expected"),
        [
            ([], ([], [])),
            (["-foo"], (["-foo"], [])),
            (["-foo", "--bar"], (["-foo", "--bar"], [])),
            (["--foo", " --   "], (["--foo"], [])),
            (["--foo", " --   ", "-baz"], (["--foo"], ["-baz"])),
            ([" --", "-baz", "-bop"], ([], ["-baz", "-bop"])),
            (["--"], ([], [])),
        ],
    )
    def test_partition_argv(
        self, argv: list[str], expected: tuple[list[str], list[str]]
    ) -> None:
        main_expected, rest_expected = expected
        main_ret, rest_ret = partition_argv(argv)
        assert main_ret == main_expected
        assert rest_ret == rest_expected


if __name__ == "__main__":
    sys.exit(pytest.main())
