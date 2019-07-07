from ._registry import find_function_by_path_name, regist


class ArgumentError(Exception):
    pass


class dispatch:
    _REGISTRY = {}

    def __init__(self, func_or_method):
        self.function_path_name = regist(func_or_method)

    def __call__(self, *args, **kwargs):
        if args:
            raise ArgumentError(
                "must provide argument names to dispatch function"
            )  # noqa

        callable_obj = find_function_by_path_name(
            self.function_path_name, arg_names=kwargs.keys()
        )
        return callable_obj(**kwargs)

    def __get__(self, obj, T):
        def method(*args, **kwargs):
            if args:
                raise ArgumentError(
                    "must provide argument names to dispatch method"
                )  # noqa

            arg_names = ["self", *kwargs.keys()]
            callable_obj = find_function_by_path_name(
                self.function_path_name, arg_names=arg_names
            )
            return callable_obj(obj, **kwargs)

        return method
