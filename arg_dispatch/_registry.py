import inspect
from collections import defaultdict

REGISTRY = defaultdict(dict)


class ExistDefaultValue(Exception):
    pass


class SignatureError(Exception):
    pass


class FunctionNotRegist(Exception):
    pass


class FrozenList(object):
    def __init__(self, items):
        self._list = items

    def __iter__(self):
        for item in self._list:
            yield item

    def __str__(self):
        return repr(self._list)

    def __repr__(self):
        return f"FrozenList({repr(self._list)})"

    def __eq__(self, other):
        return self._list == other._list

    def __hash__(self):
        return hash(str(self._list))


def gen_function_path_name(func_or_method):
    module_name = func_or_method.__module__
    class_name = func_or_method.__class__.__name__
    name = func_or_method.__name__

    path_name = f"{module_name}.{class_name}.{name}"
    return path_name


def regist(func_or_method):
    signature = inspect.signature(func_or_method)
    for param in signature.parameters.values():
        if param.kind != inspect._ParameterKind.POSITIONAL_OR_KEYWORD:
            raise SignatureError("only support positional argument")
        if param.default != inspect._empty:
            raise ExistDefaultValue(
                "does not support function with default value"
            )  # noqa

    path_name = gen_function_path_name(func_or_method)
    signature_args = FrozenList(list(signature.parameters.keys()))

    REGISTRY[path_name][signature_args] = func_or_method
    return path_name


def find_function_by_path_name(function_path_name, arg_names):
    signature_args = FrozenList(list(arg_names))
    try:
        return REGISTRY[function_path_name][signature_args]
    except KeyError:
        function_name = function_path_name.split(".")[-1]
        signature = f'{function_name}({", ".join(arg_names)})'
        raise FunctionNotRegist(f"Not Registed signature {signature}")
