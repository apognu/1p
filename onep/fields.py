from __future__ import annotations

import getpass
import secrets
import string

from enum import Enum

from .util import fatal


class FieldKind(Enum):
    PLAIN = "plain"
    SECRET = "secret"
    TOTP = "totp"

    def is_secret(self) -> bool:
        return self in [FieldKind.SECRET, FieldKind.TOTP]


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
        if self.kind == FieldKind.SECRET:
            kind = "password"
        elif self.kind == FieldKind.TOTP:
            kind = "otp"
            value = f"otpauth://totp/?secret={self.value}"
        else:
            kind = "text"

        return f"{self.key}[{kind}]={self.value}"
