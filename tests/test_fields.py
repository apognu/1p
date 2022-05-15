import mock
import pytest

from onep.fields import FieldKind, Field


def test_invalid_field(capsys):
    with pytest.raises(SystemExit) as e:
        Field.from_spec("invalid", 0, False)

    output = capsys.readouterr().err

    assert e.value.code == 1
    assert "ERROR:" in output
    assert "field spec 'invalid' is invalid" in output


def test_plain_field():
    field = Field.from_spec("key=value", 0, False)

    assert field.kind == FieldKind.PLAIN
    assert field.key == "key"
    assert field.value == "value"
    assert field.to_string() == "key[text]=value"


@mock.patch("getpass.getpass", mock.MagicMock(return_value="password"))
def test_prompt_secret():
    field = Field.from_spec("key=", 0, False)

    assert field.kind == FieldKind.SECRET
    assert field.key == "key"
    assert field.value == "password"
    assert field.to_string() == "key[password]=password"


@mock.patch("string.ascii_letters", "a")
@mock.patch("string.digits", "a")
def test_gererated_secret():
    field = Field.from_spec("key=-", 32, False)

    assert field.kind == FieldKind.SECRET
    assert field.key == "key"
    assert len(field.value) == 32
    assert field.value == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert field.to_string() == f"key[password]=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@mock.patch("string.ascii_letters", "")
@mock.patch("string.digits", "")
@mock.patch("string.punctuation", "$")
def test_gererated_secret_with_symbol():
    field = Field.from_spec("key=-", 16, True)

    assert field.kind == FieldKind.SECRET
    assert field.key == "key"
    assert len(field.value) == 16
    assert field.value == "$$$$$$$$$$$$$$$$"
    assert field.to_string() == f"key[password]=$$$$$$$$$$$$$$$$"


def test_explicit_secret():
    field = Field.from_spec("@key=value", 0, False)

    assert field.kind == FieldKind.SECRET
    assert field.key == "key"
    assert field.value == "value"
    assert field.to_string() == "key[password]=value"


def test_totp():
    field = Field.from_spec("+key=value", 0, False)

    assert field.kind == FieldKind.TOTP
    assert field.key == "key"
    assert field.value == "value"
    assert field.to_string() == "key[otp]=otpauth://totp/?secret=value"


def test_url():
    field = Field.from_spec("key=https://example.com/auth?login=apognu", 0, False)

    assert field.kind == FieldKind.URL
    assert field.key == "key"
    assert field.value == "https://example.com/auth?login=apognu"
    assert field.to_string() == "key[url]=https://example.com/auth?login=apognu"


def test_email():
    field = Field.from_spec("key=apognu@example.com", 0, False)

    assert field.kind == FieldKind.EMAIL
    assert field.key == "key"
    assert field.value == "apognu@example.com"
    assert field.to_string() == "key[email]=apognu@example.com"


def test_phone():
    field = Field.from_spec("key=+33123456789", 0, False)

    assert field.kind == FieldKind.PHONE
    assert field.key == "key"
    assert field.value == "+33123456789"
    assert field.to_string() == "key[phone]=+33123456789"
