import os
import pathlib

import pytest
from hamcrest import *


def test_project_name_applied(cookies):
    project_name = "pulse-project"
    result = cookies.bake(extra_context={"project_name": project_name})

    assert_that(result.project.basename, equal_to(project_name))


def test_package_name_applied(cookies):
    package_name = "package"
    result = cookies.bake(extra_context={"package_name": package_name})
    expected_path = pathlib.Path(result.project.strpath) / package_name

    assert_that(expected_path.exists(), is_(True))
    assert_that(expected_path.is_dir(), is_(True))


def test_version_applied(cookies):
    version = "1.15.0"
    result = cookies.bake(extra_context={"version": version})
    version_path = pathlib.Path(result.project.strpath) / "version"
    with open(version_path) as vf:
        got_version = vf.read().strip()

    assert_that(got_version, equal_to(version))

