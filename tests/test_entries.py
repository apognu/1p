import pytest
import mock

from onep.onep import main
from . import common


@common.session
@mock.patch("onep.commands.search.run", return_value=(True, "[]", ""))
def test_search_no_result(a, capsys):
    try:
        main(["personal", "search", "dummy"])
    except SystemExit:
        pass

    output = capsys.readouterr().err

    assert output == ""


ENTRIES = """[{"id": "entry1", "title": "First entry"}, {"id": "entry2", "title": "Second entry"}]"""


@common.session
@mock.patch("onep.commands.search.run", return_value=(True, ENTRIES, ""))
def test_search(a, capsys):
    try:
        main(["personal", "search", "-t", "dummy"])
    except SystemExit:
        pass

    output = capsys.readouterr().out

    assert output.count("\n") == 3
    assert "entry1" in output
    assert "First entry" in output
    assert "entry2" in output
    assert "Second entry" in output


@common.session
@mock.patch("onep.commands.search.run", return_value=(True, ENTRIES, ""))
def test_search_filter(a, capsys):
    try:
        main(["personal", "search", "-t", "dummy", "Second"])
    except SystemExit:
        pass

    output = capsys.readouterr().out

    assert output.count("\n") == 2
    assert "entry1" not in output
    assert "entry2" in output
    assert "Second entry" in output
