import mock
import pytest

from onep.onep import main
from tests import common


@common.session
@mock.patch("onep.commands.search.run", mock.MagicMock(return_value=(True, "[]", "")))
def test_search_no_result(capsys):
    try:
        main(["personal", "search", "dummy"])
    except SystemExit:
        pass

    output = capsys.readouterr().err

    assert output == ""


ENTRIES = """
  [
    {
      "id": "entry1",
      "title": "First entry"
    },
    {
      "id": "entry2",
      "title": "Second entry"}
  ]
"""


@common.session
@mock.patch("onep.commands.search.run", mock.MagicMock(return_value=(True, ENTRIES, "")))
@pytest.mark.parametrize("option", ("--tags", "-t"))
def test_search(capsys, option):
    try:
        main(["personal", "search", option, "dummy"])
    except SystemExit:
        pass

    output = capsys.readouterr().out

    assert output.count("\n") == 3
    assert "entry1" in output
    assert "First entry" in output
    assert "entry2" in output
    assert "Second entry" in output


@common.session
@mock.patch("onep.commands.search.run", mock.MagicMock(return_value=(True, ENTRIES, "")))
@pytest.mark.parametrize("option", ("--tags", "-t"))
def test_search_filter(capsys, option):
    try:
        main(["personal", "search", option, "dummy", "Second"])
    except SystemExit:
        pass

    output = capsys.readouterr().out

    assert output.count("\n") == 2
    assert "entry1" not in output
    assert "entry2" in output
    assert "Second entry" in output


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
def test_show(capsys):
    main(["-j", "personal", "show", "dummy"])

    output = capsys.readouterr().out

    assert "item get dummy" in output


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
@pytest.mark.parametrize("option", ("--fields", "-f"))
def test_show_fields(capsys, option):
    main(["-j", "personal", "show", "dummy", option, "field1,field2"])

    output = capsys.readouterr().out

    assert "item get dummy --fields=field1,field2" in output


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
@pytest.mark.parametrize("option", ("--otp", "-o"))
def test_show_fields(capsys, option):
    main(["-j", "personal", "show", "dummy", option])

    output = capsys.readouterr().out

    assert "item get dummy --otp" in output


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
@pytest.mark.parametrize("option", ("--otp", "-o"))
def test_show_select(capsys, option):
    main(["-j", "personal", "show", "dummy", option])

    output = capsys.readouterr().out

    assert "item get dummy --otp" in output
