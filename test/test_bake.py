import os
import pathlib

import pytest
from hamcrest import assert_that, equal_to, none, is_


def test_bake_project(cookies):
    result = cookies.bake()

    assert_that(result.exit_code, equal_to(0))
    assert_that(result.exception, none())
    assert_that(result.project.basename, equal_to("helloworld"))
    assert_that(result.project.isdir(), is_(True))
