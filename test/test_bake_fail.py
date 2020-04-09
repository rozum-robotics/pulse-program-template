import pathlib

from cookiecutter.exceptions import FailedHookException

import pytest
from hamcrest import assert_that, equal_to, instance_of


def test_invalid_project_name_exit_code(cookies):
    assert_that(
        cookies.bake(extra_context={"project_name": "aa-aa"}).exit_code,
        equal_to(-1)
    )


def test_invalid_project_name_exception(cookies):
    assert_that(
        cookies.bake(extra_context={"project_name": "aa-aa"}).exception,
        instance_of(FailedHookException)
    )
