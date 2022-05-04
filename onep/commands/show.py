import inquirer
import json
import sys

from ..util import exit, fatal, run


def show(session, to_json, id, tags, fields, otp, select):
    if len(id) == 0 and tags is None:
        fatal("Either tags or ID should be provided")

    if len(id) > 0:
        id = "".join(id)
    else:
        (status, stdout, stderr) = run(["item", "list", "--format=json", f"--tags={tags}"], session=session, silent=True)

        if not status:
            fatal(stderr)

        entries = json.loads(stdout)

        if len(entries) == 0:
            exit("No entry matched these filters.", file=sys.stderr)
        if not select and len(entries) > 1:
            print("WARN: Multiple entries responded to this query, showing the first", file=sys.stderr)

        if not select:
            id = entries[0]["id"]
        else:
            entry = inquirer.prompt([inquirer.List("entry", message="Select an entry", choices=list(map(lambda e: (f"{e['title']} ({e['id']})", e["id"]), entries)))])

            id = entry["entry"]

    args = ["item", "get", id]

    if fields is not None:
        args.append(f"--fields={fields}")

    if otp:
        args.append("--otp")

    run(args, json=to_json, session=session)
