# SPDX-FileCopyrightText: Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES.
#                         All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from aedifix.util.callables import classify_callable, get_calling_function

if TYPE_CHECKING:
    from collections.abc import Callable


def foo() -> Any:
    return get_calling_function()


class Foo:
    # type hinting these properly would just confuse the type hinters
    # (not to mention, recurse infinitely). So these are just any's.
    def method(self) -> Any:
        return foo()

    @classmethod
    def class_method(cls) -> Any:
        return foo()

    @property
    def prop(self) -> Any:
        return foo()

    def __call__(self) -> Any:
        return foo()


class TestGetCallingFunction:
    def test_bare_func(self) -> None:
        def bar() -> Callable[[], Any]:
            return foo()

        assert foo() == self.test_bare_func
        assert bar() == bar

    def test_class(self) -> None:
        inst = Foo()
        assert inst.method() == inst.method
        assert inst.class_method() == inst.class_method
        # Error: "Callable[[Foo], Any]" has no attribute "fget" [attr-defined]
        #
        # ... yes it obviously does you absolute dunce
        assert inst.prop == Foo.prop.fget  # type: ignore[attr-defined]
        assert inst() == inst.__call__


class TestClassifyCallable:
    def test_func(self) -> None:
        qualname, path, lineno = classify_callable(foo)
        assert qualname == "tests.util.test_callables.foo"
        assert path == Path(__file__)
        assert lineno == 18  # Unfortunately a brittle test...

        qualname, path, lineno = classify_callable(Foo().method)
        assert qualname == "tests.util.test_callables.Foo.method"
        assert path == Path(__file__)
        assert lineno == 25  # Unfortunately a brittle test...

        qualname, path, lineno = classify_callable(Foo.class_method)
        assert qualname == "tests.util.test_callables.Foo.class_method"
        assert path == Path(__file__)
        assert lineno == 28  # Unfortunately a brittle test...

        prop_function = Foo.prop.fget  # type: ignore[attr-defined]
        qualname, path, lineno = classify_callable(prop_function)
        assert qualname == "tests.util.test_callables.Foo.prop"
        assert path == Path(__file__)
        assert lineno == 32  # Unfortunately a brittle test...

        qualname, path, lineno = classify_callable(Foo().__call__)
        assert qualname == "tests.util.test_callables.Foo.__call__"
        assert path == Path(__file__)
        assert lineno == 36  # Unfortunately a brittle test...


if __name__ == "__main__":
    sys.exit(pytest.main())
