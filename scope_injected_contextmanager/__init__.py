__author__ = "sloev"
__email__ = "johannes.valbjorn@gmail.com"
__version__ = "0.0.1"

import inspect
import sys
from contextlib import contextmanager


def _create_key_error_stack_trace_formatter(frame, func):
    def format_keyerror_stacktrace(kind, key_error, traceback):
        first_missing_key = str(key_error).strip("'")
        caller_traceback = inspect.getframeinfo(frame)
        exc = AttributeError(
            f'Function "{func.__name__}" is missing the variable "{first_missing_key}". '
            + f'It should have been declared in File "{caller_traceback.filename}", '
            + f"line {caller_traceback.lineno}, in {caller_traceback.function}"
        )
        sys.__excepthook__(AttributeError, exc, caller_traceback)

    @contextmanager
    def handle_keyerror():
        sys.excepthook = format_keyerror_stacktrace
        yield
        sys.excepthook = sys.__excepthook__

    return handle_keyerror()


def scope_injected_contextmanager(func):
    """
    scope_injected_contextmanager takes a function and returns context manager

    simple example:
        from scope_injected_contextmanager import scope_injected_contextmanager

        fetch = lambda request: ('ok', 200)

        @scope_injected_contextmanager
        def log_request(request, response):
            print(f"request: {request} response: {response}")

        with log_request:
            request = {
                'query_args': {
                    'foo': 10
                }
            }
            response = fetch(request)

        # prints
        # request: {'query_args': {'foo': 10}} response: ('ok', 200)
    """

    signature = inspect.getfullargspec(func)
    func_arg_names = signature.args
    defaults = signature.defaults or tuple()
    func_arg_names = func_arg_names[: len(func_arg_names) - len(defaults)]

    class ScopeInjectedContextManager:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __call__(self, *args, **kwargs):
            return ScopeInjectedContextManager(*args, **kwargs).__enter__()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            frame = inspect.currentframe().f_back
            inner_locals_copy = frame.f_locals.copy()
            exception = None
            args = tuple(self.args)
            kwargs = dict(**self.kwargs)
            with _create_key_error_stack_trace_formatter(frame, func):
                kwargs.update({k: inner_locals_copy[k] for k in func_arg_names})
            func(*args, **kwargs)

    return ScopeInjectedContextManager()
