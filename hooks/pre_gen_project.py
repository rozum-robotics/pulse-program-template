import re
import sys

PACKAGE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

project_name = "{{cookiecutter.project_name}}"

if not re.match(PACKAGE_REGEX, project_name):
    print("ERROR: {} is not a valid Python package name!".format(project_name))
    sys.exit(1)
