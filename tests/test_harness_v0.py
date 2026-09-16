import sys

from harness.runner import classify_failure, run_command

#Harness 自身的最小测试
def test_run_command_success():
    result = run_command(sys.path[0], [sys.executable, "-c", "print('ok')"])

    assert result.passed is True
    assert result.return_code == 0
    assert result.stdout.strip() == "ok"
    assert result.error_type is None


def test_classify_assertion_failure():
    assert classify_failure("", "AssertionError: wrong result", 1) == "AssertionError"


def test_run_command_timeout():
    result = run_command(
        sys.path[0],
        [sys.executable, "-c", "import time; time.sleep(0.2)"],
        timeout_seconds=0.01,
    )

    assert result.passed is False
    assert result.timed_out is True
    assert result.error_type == "TimeoutExpired"
