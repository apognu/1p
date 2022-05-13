import sys

from argparse import ArgumentParser, Namespace, BooleanOptionalAction

from .util import init_secret_storage, check_session, fatal
from .colors import *
from onep.commands import *


def main() -> None:
    init_secret_storage()

    args = parse_args()

    if args.command is None:
        fatal("no command provided")

    if args.command != "signin":
        session = check_session(args.account)

        if session is None:
            sys.exit(1)

    assert session is not None

    if args.command == "signin":
        signin(args.account)
    elif args.command == "vaults":
        vaults(session, args.json)
    elif args.command == "vault":
        vault(session, args.json, args.id)
    elif args.command == "search":
        search(session, args.json, args.vault, args.tags, args.term)
    elif args.command == "show":
        show(session, args.json, args.id, args.tags, args.fields, args.otp, args.select)
    elif args.command == "create":
        create(session, args.vault, args.category, args.title, args.fields, args.tags, args.password_length, args.symbols)
    elif args.command == "edit":
        edit(session, args.id, args.fields, args.tags, args.delete, args.password_length, args.symbols)
    elif args.command == "delete":
        delete(session, args.archive, args.id)
    elif args.command == "download":
        download(session, args.title)
    elif args.command == "upload":
        upload(session, args.vault, args.title, args.file, args.filename)
    elif args.command == "share":
        share(session, args.id, args.time, args.once)


def parse_args() -> Namespace:
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

    return cli.parse_args()
