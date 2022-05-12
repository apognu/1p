# 1p - 1Password CLI helper

`1p` is a wrapper around 1Password's `op` CLI tool to give a more user-friendly interface to secret retrieval.

Requires Python >= 3.7.

It opens a session with 1Password and stores the session token in the system's keyring, optionally, you can run with `ONEP_SECRET_BACKEND=plain` to store it under `~/.cache/1p`.

It requires that the configured 1Password account has a shorthand defined (when using `op account add`).

## Installation

```shell
$ # From PyPI
$ pip install onep

$ # Development build from GitHub
$ https://github.com/apognu/1p/releases/download/tip/onep-tip-py3-none-any.whl
```

## Usage

```shell
$ 1p --help
usage: 1p [-h] [-j] ACCOUNT COMMAND ...

positional arguments:
  ACCOUNT     shorthand of the 1Password account
  COMMAND
    signin    authenticate into a 1Password account
    vaults    list available vaults
    vault     show information about a vault
    search    search entries matching provided term
    show      display an entry
    create    create an entry
    edit      edit an entry
    delete    delete an entry
    share     get a shareable link to an item

options:
  -h, --help  show this help message and exit
  -j, --json  format output as JSON

$ 1p personal search -t social
ID                            TITLE
__________________________    GitHub
__________________________    Twitter
```
