import json
import os
import sys

from argparse import ArgumentParser
from os import path

from .util import init_secret_storage, check_session, fatal
from . import commands


def main():
    init_secret_storage()

    args = parse_args()

    if args.command is None:
        fatal("ERROR: no command provided")

    if args.command != "signin":
        session = check_session(args.account)

        if session is None:
            sys.exit(1)

    match args.command:
        case "signin":
            commands.signin(args.account)
        case "vaults":
            commands.vaults(session, args.json)
        case "vault":
            commands.vault(session, args.json, args.id)
        case "search":
            commands.search(session, args.json, args.vault, args.tags, args.term)
        case "show":
            commands.show(session, args.json, args.id, args.tags, args.fields, args.otp, args.select)
        case "share":
            commands.share(session, args.id, args.time, args.once)


def parse_args():
    cli = ArgumentParser(prog="1p")
    cli.add_argument("-j", "--json", action="store_true")
    cli.add_argument("account", metavar="ACCOUNT")

    commands = cli.add_subparsers(dest="command", metavar="COMMAND")

    commands.add_parser("signin", help="Authenticate into a 1Password account")
    commands.add_parser("vaults", help="List available vaults")

    cmd_vault = commands.add_parser("vault", help="Show information about a vault")
    cmd_vault.add_argument("id", metavar="ID")

    cmd_search = commands.add_parser("search", help="Search entries matching provided term")
    cmd_search.add_argument("-v", "--vault", type=str, metavar="VAULT")
    cmd_search.add_argument("-t", "--tags", type=str, metavar="TAGS")
    cmd_search.add_argument("-s", "--term", type=str, metavar="TERM")

    cmd_show = commands.add_parser("show", help="Display an entry")
    cmd_show_target = cmd_show.add_mutually_exclusive_group(required=True)
    cmd_show_target.add_argument("id", metavar="ID", nargs="*", default=[])
    cmd_show_target.add_argument("-t", "--tags", type=str, metavar="TAGS")
    cmd_show.add_argument("-f", "--fields", type=str, metavar="FIELDS")
    cmd_show.add_argument("-o", "--otp", action="store_true")
    cmd_show.add_argument("-s", "--select", action="store_true")

    cmd_share = commands.add_parser("share", help="Get a shareable link to an item")
    cmd_share.add_argument("id", metavar="ID")
    cmd_share.add_argument("-t", "--time", type=str, metavar="EXPIRY")
    cmd_share.add_argument("-o", "--once", action="store_true")

    return cli.parse_args()
