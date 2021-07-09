#!/usr/bin/env python3

"""This module contain a list subcommand for the docker-image resource."""

def configure_parser(os_subparser):
    """Adds the parser for the list command to an argparse ArgumentParser"""
    os_subparser.add_parser(
        "list", help="List operating systems presents on instance"
    )


def subcommand(api):
    """Execute the list command with args."""
    operating_systems = api.operating_systems()
    os_format_string = (
        "{key:15.15} "
        "{short_name:20.20} "
        "{arch:8.8} "
    )
    print(
        os_format_string.format(
            key="KEY",
            short_name="NAME",
            arch="ARCH"
        )
    )
    for operating_system in operating_systems:
        print(
            os_format_string.format(
                key=operating_system.key,
                short_name=operating_system.short_name,
                arch=operating_system.arch or ""
            )
        )
