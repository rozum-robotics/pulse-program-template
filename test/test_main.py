import sys
import pytest
from hamcrest import *


def test_main_run(cookies):
    result = cookies.bake()
    sys.path.append(result.project.strpath)
    pulse_program = __import__("pulse_program", fromlist=["main"])
    pulse_program.main.run(1)


def test_methods_invocation(cookies, mocker):
    result = cookies.bake()
    sys.path.append(result.project.strpath)
    pulse_program = __import__("pulse_program", fromlist=["main", "program"])
    program_patch = mocker.patch.object(pulse_program.main, "program")
    iterations = 2
    pulse_program.main.run(iterations)
    call = mocker.call
    
    program_patch.assert_has_calls([
        call.before_all(),
        
        call.before_each(),
        call.execute(),
        call.after_each(),
        
        call.before_each(),
        call.execute(),
        call.after_each(),
        
        call.after_all()
    ])
    program_patch.on_error.assert_not_called()


def test_on_error_invocation(cookies, mocker):
    result = cookies.bake()
    sys.path.append(result.project.strpath)
    pulse_program = __import__("pulse_program", fromlist=["main", "program"])
    program_patch = mocker.patch.object(pulse_program.main, "program")
    program_patch.execute.side_effect = Exception("Boom!")
    pulse_program.main.run(1)
    
    program_patch.on_error.assert_called_once()
