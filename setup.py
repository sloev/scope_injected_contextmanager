#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os

readme = open("README.md", "r").read()

metadata = {}
version_filename = os.path.join(
    os.path.dirname(__file__), "scope_injected_contextmanager", "__init__.py"
)
exec(open(version_filename).read(), None, metadata)

test_requirements = [
    "pytest",
    "pytest-readme>=1.0.0",
]

setup(
    name="scope_injected_contextmanager",
    version=metadata["__version__"],
    description="A decorator/context manager that injects scope vars into a function",
    long_description=readme,
    long_description_content_type="text/markdown",
    author=metadata["__author__"],
    author_email=metadata["__email__"],
    url="https://github.com/sloev/scope_injected_contextmanager",
    packages=["scope_injected_contextmanager",],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="contextmanager decorator scope inject",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
