import mock
import pytest

from onep.util import run


@mock.patch("onep.util.OP_COMMAND", "echo")
def test_run_simple(capsys):
    run(["dummy", "arguments", "--flag", "value"])

    output = capsys.readouterr().out

    assert "dummy arguments --flag value" in output


@mock.patch("onep.util.OP_COMMAND", "ls")
def test_run_error(capsys):
    (status, _, stderr) = run(["/non/existent"])

    output = capsys.readouterr().err

    assert not status
    assert "No such file or directory" in stderr
    assert "No such file or directory" in output


@mock.patch("onep.util.OP_COMMAND", "echo")
def test_run_args(capsys):
    run(["dummy", "arguments", "--flag", "value"], session="dummysession", json=True)

    output = capsys.readouterr().out

    assert "dummy arguments --flag value --session=dummysession --format=json" in output


@mock.patch("onep.util.OP_COMMAND", "ls")
def test_run_silent(capsys):
    (status, stdout, _) = run(["/etc"], silent=True)

    output = capsys.readouterr().out

    assert status
    assert "passwd" in stdout
    assert output == ""


@mock.patch("onep.util.OP_COMMAND", "cat")
def test_run_stdin(capsys):
    input = "dummyinput"

    (status, stdout, _) = run([], stdin=input)

    output = capsys.readouterr().out

    assert status
    assert "dummyinput" in stdout
    assert "dummyinput" in output
