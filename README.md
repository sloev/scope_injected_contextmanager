# Scope Injected ContextManager

A decorator/context manager that injects scope vars into a function

* A context manager decorator for **Python 3**
* Lets you specify variables to extract from the innner-scope (the managed scope)
and will inject them into the `@scope_injected_contextmanager` decorated function
* acts like a defaulted function *(think functools.partial)*
* allows you to pass in kwargs at runtime as well

## Usage

*For an extensive collection of examples see [tests](./tests/test_all.py)*

Functions decorated with `@scope_injected_contextmanager` becomes context managers that can be invoked in two different ways:

**As an instance** 
```python
from scope_injected_contextmanager import scope_injected_contextmanager
@scope_injected_contextmanager
def decorated_function(): pass

with decorated_function:
    something = 100
```

**Or as a function**

```python
from scope_injected_contextmanager import scope_injected_contextmanager
@scope_injected_contextmanager
def decorated_function(): pass

with decorated_function():
    something = 100
```

### Simple example

```python

from scope_injected_contextmanager import scope_injected_contextmanager

fetch = lambda request: ("ok", 200)

@scope_injected_contextmanager
def log_request(request, response):
    print(f"request: {request} response: {response}")

with log_request:
    request = {
        "query_args": {
            'foo': 10
        }
    }
    response = fetch(request)

# prints
# request: {'query_args': {'foo': 10}} response: ('ok', 200)
```

### Advanced example

```python

from scope_injected_contextmanager import scope_injected_contextmanager

fetch = lambda request: ("ok", 200)

@scope_injected_contextmanager
def log_request(request, response, some_explicit_variable=None):
    print(f"request: {request} response: {response} some_explicit_variable: {some_explicit_variable}")

with log_request(some_explicit_variable="foo):
    request = {
        "query_args": {
            'foo': 10
        }
    }
    response = fetch(request)

# prints
# request: {'query_args': {'foo': 10}} response: ('ok', 200) some_explicit_variable: foo
```

## why?

I needed a low-on-syntax context-manager that would log request_args and response.
When looking at implementing it i ran into this issue, and asked for help: 
["Spooky action observed in Python context manager"](https://stackoverflow.com/questions/60270909/spooky-action-observed-in-python-context-manager)

I was let down by the fact that you apparently can't give a context manager access to your variables.

Thats why i hacked this together ;-)

## Testing

see [tests](./tests/test_all.py)

run `make setup-all tox` on a (linux or osx) with [pyenv](https://github.com/pyenv/pyenv#installation) installed.
