import pathlib

from cookiecutter.exceptions import FailedHookException

import pytest
from hamcrest import *


def test_invalid_package_name(cookies):
    package_name = "aa-aa"
    result = cookies.bake(extra_context={"package_name": package_name})

    assert_that(result.exit_code, equal_to(-1))
    assert_that(result.exception, instance_of(FailedHookException))
