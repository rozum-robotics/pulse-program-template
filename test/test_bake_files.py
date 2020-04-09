import os
import pathlib

import pytest
from hamcrest import assert_that, has_items


def test_build_files_added(cookies):
    result = cookies.bake()
    project_files = os.listdir(result.project.strpath)
    project_files = project_files + os.listdir(
        pathlib.Path(result.project.strpath) / "requirements"
    )

    assert_that(
        project_files,
        has_items(
            "setup.py",
            "version",
            "MANIFEST.in",
            "requirements",
            "development.txt",
            "production.txt",
        ),
    )


def test_package_files_added(cookies):
    result = cookies.bake()
    package_files = os.listdir(
        pathlib.Path(result.project.strpath) / "helloworld"
    )

    assert_that(
        package_files, has_items("main.py", "__init__.py", "program.py")
    )