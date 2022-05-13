from __future__ import annotations

import getpass
import phonenumbers
import secrets
import string
import validators  # type: ignore

from enum import Enum
from urllib.parse import urlparse

from .util import fatal


class FieldKind(Enum):
    PLAIN = "text"
    SECRET = "password"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    TOTP = "otp"

    def is_secret(self) -> bool:
        return self in [FieldKind.SECRET, FieldKind.TOTP]


def is_url(value: str) -> bool:
    try:
        result = urlparse(value)

        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_phone_number(value: str) -> bool:
    try:
        result = phonenumbers.parse(value)

        return phonenumbers.is_possible_number(result)
    except phonenumbers.NumberParseException:
        return False


class Field:
    kind: FieldKind
    key: str
    value: str

    def __init__(self, kind: FieldKind, key: str, value: str):
        self.kind = kind
        self.key = key
        self.value = value

    @classmethod
    def from_spec(cls, spec: str, length: int, symbols: bool) -> Field:
        if "=" not in spec:
            fatal(f"field spec '{spec}' is invalid")

        kind = FieldKind.PLAIN
        [key, value] = spec.split("=", maxsplit=1)

        if key.startswith("@"):
            kind = FieldKind.SECRET
            key = key.lstrip("@")
        elif key.startswith("+"):
            kind = FieldKind.TOTP
            key = key.lstrip("+")
        elif is_url(value):
            kind = FieldKind.URL
        elif validators.email(value):
            kind = FieldKind.EMAIL
        elif is_phone_number(value):
            kind = FieldKind.PHONE

        if value == "":
            if not kind.is_secret():
                kind = FieldKind.SECRET

            value = getpass.getpass(f'Secret value for "{key}": ')
        elif value == "-":
            if kind == FieldKind.TOTP:
                fatal("TOTP field value cannot be generated")

            alphabet = string.ascii_letters + string.digits

            if symbols:
                alphabet = alphabet + string.punctuation

            kind = FieldKind.SECRET
            value = "".join(secrets.choice(alphabet) for i in range(length))

        return Field(kind, key, value)

    def to_string(self) -> str:
        if self.kind == FieldKind.TOTP:
            self.value = f"otpauth://totp/?secret={self.value}"

        return f"{self.key}[{self.kind.value}]={self.value}"
