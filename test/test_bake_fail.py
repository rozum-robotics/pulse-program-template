import pathlib

from cookiecutter.exceptions import FailedHookException

import pytest
from hamcrest import assert_that, equal_to, instance_of


def test_invalid_project_name(cookies):
    project_name = "aa-aa"
    result = cookies.bake(extra_context={"project_name": project_name})

    assert_that(result.exit_code, equal_to(-1))
    assert_that(result.exception, instance_of(FailedHookException))
