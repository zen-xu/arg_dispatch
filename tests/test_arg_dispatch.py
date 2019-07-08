import pytest
from arg_dispatch import __version__, dispatch
from arg_dispatch import _registry
from arg_dispatch._arg_dispatch import ArgumentError


def test_version():
    assert __version__ == "0.1.3"


@dispatch
def demo(a, b):
    return a + b


@dispatch  # noqa
def demo(c):
    return c


def test_function():
    assert demo(a=1, b=2) == 3
    assert demo(c=4) == 4


def test_function_with_default():
    with pytest.raises(_registry.ExistDefaultValue):

        @dispatch
        def demo(a, d=1):
            return "error"


def test_call_function_without_argument_name():
    with pytest.raises(ArgumentError):
        demo(1, 2)


def test_function_not_regist():
    with pytest.raises(_registry.FunctionNotRegist):
        demo(a=1, b=2, c=3)


class Demo(object):
    @dispatch
    def demo(self, a, b):
        return a + b

    @dispatch  # noqa
    def demo(self, c):
        return c


def test_method():
    obj = Demo()
    assert obj.demo(a=100, b=200) == 300
    assert obj.demo(c=400) == 400


def test_call_method_without_argument_name():
    obj = Demo()
    with pytest.raises(ArgumentError):
        obj.demo(1, 2)


def test_method_not_regist():
    obj = Demo()
    with pytest.raises(_registry.FunctionNotRegist):
        obj.demo(a=1, b=2, c=3)
