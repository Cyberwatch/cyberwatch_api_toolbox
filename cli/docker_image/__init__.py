#!/usr/bin/env python3

"""This module contains all the commands related to docker images."""

import sys
from . import create, list_images, update, show, scan


def configure_parser(subparser):
    """Adds the `docker-image` subcommand to an argparse ArgumentParser
    object"""
    docker_image_parser = subparser.add_parser(
        "docker-image", help="Interact with docker images"
    )
    docker_image_subparser = docker_image_parser.add_subparsers(
        dest="action", help="Actions on docker images"
    )
    docker_image_subparser.required = True

    create.configure_parser(docker_image_subparser)
    list_images.configure_parser(docker_image_subparser)
    update.configure_parser(docker_image_subparser)
    show.configure_parser(docker_image_subparser)
    scan.configure_parser(docker_image_subparser)


def subcommand(args, api):
    """Execute the right docker-image subcommand from args."""
    if args.action == "create":
        create.subcommand(args, api)
    elif args.action == "list":
        list_images.subcommand(api)
    elif args.action == "scan":
        scan.subcommand(args, api)
    elif args.action == "show":
        show.subcommand(args, api)
    elif args.action == "update":
        update.subcommand(args, api)
    else:
        print(
            f"'{args.action}' is not a valid subcommand of docker-image",
            file=sys.stderr,
        )
        sys.exit(1)
