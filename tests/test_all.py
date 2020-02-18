import pytest
from scope_injected_contextmanager import scope_injected_contextmanager


@scope_injected_contextmanager
def log_request(request, response):
    print(f"request: {request} response: {response}")


@scope_injected_contextmanager
def log_request_with_kwargs(request, response, something_else=None):
    print(f"request: {request} response: {response} something_else: {something_else}")


@scope_injected_contextmanager
def broken_log_request(request, response):
    raise Exception("broken log request")


def test_log_request(capsys):
    with log_request:
        request = 10
        response = 20
    captured = capsys.readouterr()
    assert captured.out == "request: 10 response: 20\n"


def test_log_request_with_kwargs(capsys):
    with log_request_with_kwargs(something_else=30):
        request = 10
        response = 20
    captured = capsys.readouterr()
    assert captured.out == "request: 10 response: 20 something_else: 30\n"


def test_log_broken_log_request(capsys):
    with pytest.raises(Exception) as e:
        with broken_log_request():
            request = 10
            response = 20
    assert str(e.value) == "broken log request"
