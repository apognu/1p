import json
import sys

from ..util import exit, fatal, run, create_table


def vaults(session: str, to_json: bool) -> None:
    (status, stdout, stderr) = run(["vault", "list", f"--session={session}"], json=True, silent=True)

    if not status:
        fatal(stderr)

    if to_json:
        print(stdout)
        sys.exit(0)

    vaults = json.loads(stdout)

    if len(vaults) == 0:
        exit("There are no vaults in this account.")

    table = create_table(["ID", "NAME"])
    table.add_rows(list(map(lambda vault: [vault["id"], vault["name"]], vaults)))

    print(table)


def vault(session: str, to_json: bool, id: str) -> None:
    run(["vault", "get", id, f"--session={session}"], json=to_json)
