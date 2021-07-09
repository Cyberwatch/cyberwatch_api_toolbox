#!/usr/bin/env python3

"""This module contains all the commands related to os assets."""

import sys
from . import list_os


def configure_parser(subparser):
    """Adds the `os` subcommand to an argparse ArgumentParser
    object"""
    os_parser = subparser.add_parser("os", help="Interact with operating systems")
    os_subparser = os_parser.add_subparsers(
        dest="action", help="Actions on operating systems"
    )
    os_subparser.required = True

    list_os.configure_parser(os_subparser)


def subcommand(args, api):
    """Execute the right airgap subcommand from args."""
    if args.action == "list":
        list_os.subcommand(api)
    else:
        print(
            f"'{args.action}' is not a valid subcommand for os",
            file=sys.stderr,
        )
        sys.exit(1)
