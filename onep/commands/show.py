import inquirer  # type: ignore
import json
import sys

from ..util import exit, fatal, run
from ..colors import *


def show(session: str, to_json: bool, id: str, tags: str, fields: str, otp: bool, select: bool) -> None:
    if len(id) > 0:
        id = " ".join(id)
    else:
        (status, stdout, stderr) = run(["item", "list", "--format=json", f"--tags={tags}"], session=session, silent=True)

        if not status:
            fatal(stderr)

        entries = json.loads(stdout)

        if len(entries) == 0:
            exit("No entry matched these filters.")
        if not select and len(entries) > 1:
            print(f"{yellow('WARN')}: Multiple entries responded to this query, showing the first", file=sys.stderr)

        if not select:
            id = entries[0]["id"]
        else:
            entries = list(map(lambda e: (f"{e['title']} ({e['id']})", e["id"]), sorted(entries, key=lambda entry: entry["title"])))  # type: ignore
            entry = inquirer.prompt([inquirer.List("entry", message="Select an entry", choices=entries)])

            id = entry["entry"]

    args = ["item", "get", id]

    if fields is not None:
        args.append(f"--fields={fields}")

    if otp:
        args.append("--otp")

    run(args, json=to_json, session=session)
