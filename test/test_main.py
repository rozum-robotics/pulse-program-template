import sys
import pytest
from hamcrest import *


def test_main_run(cookies):
    sys.path.append(cookies.bake().project.strpath)
    pulse_program = __import__("pulse_program", fromlist=["main"])
    pulse_program.main.run(1, "localhost:8081")


def test_methods_invocation(cookies, mocker):
    sys.path.append(cookies.bake().project.strpath)
    pulse_program = __import__("pulse_program", fromlist=["main", "program"])
    program_patch = mocker.patch.object(pulse_program.main.program, "Instance")
    iterations = 2
    pulse_program.main.run(iterations, "localhost:8081")
    
    instance = program_patch.return_value
    call = mocker.call
    call_enter = call.__enter__()
    
    instance.assert_has_calls([
        call_enter.before_all(),
        
        call_enter.before_each(),
        call_enter.execute(),
        call_enter.after_each(),
        
        call_enter.before_each(),
        call_enter.execute(),
        call_enter.after_each(),
        
        call_enter.after_all()
        
    ])
    instance.on_error.assert_not_called()


def test_on_error_exit_invocation(cookies, mocker):
    sys.path.append(cookies.bake().project.strpath)
    pulse_program = __import__("pulse_program", fromlist=["main", "program"])
    program_patch = mocker.patch.object(pulse_program.main.program, "Instance")
    exception = Exception("Boom!")
    program_patch.return_value.__enter__.return_value.execute.side_effect = exception
    try:
        pulse_program.main.run(1, "localhost:8081")
    except:
        instance = program_patch.return_value
        instance.__exit__.assert_called_once()
        assert None not in instance.__exit__.call_args
