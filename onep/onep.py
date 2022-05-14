import sys

from typing import List, Optional
from argparse import ArgumentParser, Namespace, BooleanOptionalAction

from onep import commands

from .util import init_secret_storage, check_session, fatal
from .colors import *


def main(args: Optional[List[str]] = None) -> None:
    init_secret_storage()

    cli = parse_args(args)

    if cli.command is None:
        fatal("no command provided")

    if cli.command != "signin":
        session = check_session(cli.account)

        if session is None:
            sys.exit(1)

    assert session is not None

    if cli.command == "signin":
        commands.signin.signin(cli.account)
    elif cli.command == "vaults":
        commands.vaults.vaults(session, cli.json)
    elif cli.command == "vault":
        commands.vaults.vault(session, cli.json, cli.id)
    elif cli.command == "search":
        commands.search.search(session, cli.json, cli.vault, cli.tags, cli.term)
    elif cli.command == "show":
        commands.show.show(session, cli.json, cli.id, cli.tags, cli.fields, cli.otp, cli.select)
    elif cli.command == "create":
        commands.edit.create(session, cli.vault, cli.category, cli.title, cli.fields, cli.tags, cli.password_length, cli.symbols)
    elif cli.command == "edit":
        commands.edit.edit(session, cli.id, cli.fields, cli.tags, cli.delete, cli.password_length, cli.symbols)
    elif cli.command == "delete":
        commands.delete.delete(session, cli.archive, cli.id)
    elif cli.command == "download":
        commands.document.download(session, cli.title)
    elif cli.command == "upload":
        commands.document.upload(session, cli.vault, cli.title, cli.file, cli.filename)
    elif cli.command == "share":
        commands.share.share(session, cli.id, cli.time, cli.once)


def parse_args(args: Optional[List[str]]) -> Namespace:
    cli = ArgumentParser(prog="1p")
    cli.add_argument("-j", "--json", action="store_true", help="format output as JSON")
    cli.add_argument("account", metavar="ACCOUNT", help="shorthand of the 1Password account")

    commands = cli.add_subparsers(dest="command", metavar="COMMAND")

    commands.add_parser("signin", help="authenticate into a 1Password account")
    commands.add_parser("vaults", help="list available vaults")

    cmd_vault = commands.add_parser("vault", help="show information about a vault")
    cmd_vault.add_argument("id", metavar="ID")

    cmd_search = commands.add_parser("search", help="search entries matching provided term")
    cmd_search.add_argument("-v", "--vault", type=str, metavar="VAULT")
    cmd_search.add_argument("-t", "--tags", type=str, metavar="TAGS")
    cmd_search.add_argument("term", metavar="TERM", nargs="*", default=[])

    cmd_show = commands.add_parser("show", help="display an entry")
    cmd_show_target = cmd_show.add_mutually_exclusive_group(required=True)
    cmd_show_target.add_argument("id", metavar="ID", nargs="*", default=[])
    cmd_show_target.add_argument("-t", "--tags", type=str, metavar="TAGS")
    cmd_show.add_argument("-f", "--fields", type=str, metavar="FIELDS")
    cmd_show.add_argument("-o", "--otp", action="store_true")
    cmd_show.add_argument("-s", "--select", action="store_true")

    cmd_create = commands.add_parser("create", help="create an entry")
    cmd_create.add_argument("-v", "--vault", type=str, metavar="VAULT", required=True)
    cmd_create.add_argument("-c", "--category", type=str, metavar="CATEGORY", default="login")
    cmd_create.add_argument("-u", "--url", type=str, metavar="URL")
    cmd_create.add_argument("-t", "--tags", type=str, metavar="TAGS")
    cmd_create.add_argument("--password-length", type=int, default=32)
    cmd_create.add_argument("--symbols", type=bool, action=BooleanOptionalAction, default=True)
    cmd_create.add_argument("title", metavar="TITLE")
    cmd_create.add_argument("fields", metavar="FIELD", nargs="+")

    cmd_edit = commands.add_parser("edit", help="edit an entry")
    cmd_edit.add_argument("-t", "--tags", type=str, metavar="TAGS")
    cmd_edit.add_argument("-d", "--delete", type=str, action="append", metavar="FIELD")
    cmd_edit.add_argument("--password-length", type=int, default=32)
    cmd_edit.add_argument("--symbols", type=bool, action=BooleanOptionalAction, default=True)
    cmd_edit.add_argument("id", metavar="ID")
    cmd_edit.add_argument("fields", metavar="FIELD", nargs="*")

    cmd_delete = commands.add_parser("delete", help="delete an entry")
    cmd_delete.add_argument("-a", "--archive", action="store_true")
    cmd_delete.add_argument("id", metavar="ID")

    cmd_download = commands.add_parser("download", help="download a document")
    cmd_download.add_argument("title", metavar="TITLE")

    cmd_upload = commands.add_parser("upload", help="upload a document")
    cmd_upload.add_argument("-v", "--vault", type=str, metavar="VAULT", required=True)
    cmd_upload.add_argument("-f", "--filename", type=str, metavar="FILENAME")
    cmd_upload.add_argument("title", metavar="TITLE")
    cmd_upload.add_argument("file", metavar="FILE")

    cmd_share = commands.add_parser("share", help="get a shareable link to an item")
    cmd_share.add_argument("id", metavar="ID")
    cmd_share.add_argument("-t", "--time", type=str, metavar="EXPIRY")
    cmd_share.add_argument("-o", "--once", action="store_true")

    return cli.parse_args(args)
