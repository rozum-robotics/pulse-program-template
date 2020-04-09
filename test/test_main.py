import sys
import pytest

from hamcrest import assert_that, is_not, has_item


@pytest.fixture()
def mocked_program_instance_call(cookies, mocker):
    sys.path.append(cookies.bake().project.strpath)
    pulse_program = __import__("helloworld", fromlist=["main", "program"])
    program_patch = mocker.patch.object(pulse_program.main.program, "Instance")
    iterations = 2
    pulse_program.main.run(iterations, "localhost:8081")
    return program_patch.return_value


@pytest.fixture()
def exceptioned_program_instance_call(cookies, mocker):
    sys.path.append(cookies.bake().project.strpath)
    pulse_program = __import__("helloworld", fromlist=["main", "program"])
    program_patch = mocker.patch.object(pulse_program.main.program, "Instance")
    exception = Exception("Boom!")
    program_patch.return_value.__enter__.return_value.execute.side_effect = (
        exception
    )
    try:
        pulse_program.main.run(1, "localhost:8081")
    except:
        return program_patch.return_value


def test_main_run(cookies):
    sys.path.append(cookies.bake().project.strpath)
    pulse_program = __import__("helloworld", fromlist=["main"])
    pulse_program.main.run(1, "localhost:8081")


def test_methods_invocation_is_in_order(mocked_program_instance_call, mocker):
    call_enter = mocker.call.__enter__()

    mocked_program_instance_call.assert_has_calls(
        [
            call_enter.before_all(),
            call_enter.before_each(),
            call_enter.execute(),
            call_enter.after_each(),
            call_enter.before_each(),
            call_enter.execute(),
            call_enter.after_each(),
            call_enter.after_all(),
        ]
    )


def test_on_error_is_not_called(mocked_program_instance_call):
    mocked_program_instance_call.on_error.assert_not_called()


def test_on_error_exit_invoked_once(exceptioned_program_instance_call):
    exceptioned_program_instance_call.__exit__.assert_called_once()


def test_exit_call_has_exception_args(exceptioned_program_instance_call):
    assert_that(
        exceptioned_program_instance_call.__exit__.call_args,
        is_not(has_item(None)),
    )
