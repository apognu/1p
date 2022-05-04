import json
import sys

from ..util import exit, fatal, run


def search(session: str, to_json: bool, vault: str, tags: str, term: str) -> None:
    args = ["item", "list", "--format=json"]

    if vault is not None:
        args.append(f"--vault={vault}")

    if tags is not None:
        args.append(f"--tags={tags}")

    (status, stdout, stderr) = run(args, session=session, json=to_json, silent=True)

    if not status:
        fatal(stderr)

    entries = json.loads(stdout)

    if term is not None:
        entries = list(filter(lambda entry: term.lower() in entry["title"].lower(), entries))

    entries = list(map(lambda entry: [entry["id"], entry["title"]], entries))

    if len(entries) == 0:
        exit("No entry matched these filters.")

    print("{:26}    {}".format(*["ID", "TITLE"]))

    for entry in entries:
        print("{:26}    {}".format(*entry))
