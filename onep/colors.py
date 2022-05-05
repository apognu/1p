from termcolor import colored


def red(string: str) -> str:
    return colored(string, "red")


def yellow(string: str) -> str:
    return colored(string, "yellow")


def blue(string: str) -> str:
    return colored(string, "blue")


def green(string: str) -> str:
    return colored(string, "green")
