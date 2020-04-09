import os
import pathlib

import pytest
from hamcrest import assert_that, equal_to, none, is_


def test_baked_project_exit_code(cookies):
    assert_that(cookies.bake().exit_code, equal_to(0))
   

def test_baked_project_has_no_exceptions(cookies):
     assert_that(cookies.bake().exception, none())


def test_baked_project_basename(cookies):
    assert_that(cookies.bake().project.basename, equal_to("helloworld"))


def test_baked_project_isdir(cookies):
    assert_that(cookies.bake().project.isdir(), is_(True))
