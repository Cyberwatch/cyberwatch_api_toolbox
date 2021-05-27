#!/usr/bin/env python3

"""This module contains all the commands related to airgaps assets."""

import sys
from . import download_scripts, upload, download_compliance_scripts, upload_compliance


def configure_parser(subparser):
    """Adds the `airgap` subcommand to an argparse ArgumentParser
    object"""
    airgap_parser = subparser.add_parser("airgap", help="Interact with airgap")
    airgap_subparser = airgap_parser.add_subparsers(
        dest="action", help="Actions on airgap"
    )
    airgap_subparser.required = True

    download_scripts.configure_parser(airgap_subparser)
    upload.configure_parser(airgap_subparser)
    upload_compliance.configure_parser(airgap_subparser)
    download_compliance_scripts.configure_parser(airgap_subparser)


def subcommand(args, api):
    """Execute the right airgap subcommand from args."""
    if args.action == "download-scripts":
        download_scripts.subcommand(args, api)
    elif args.action == "upload":
        upload.subcommand(args, api)
    elif args.action == "download-compliance-scripts":
        download_compliance_scripts.subcommand(args, api)
    elif args.action == "upload-compliance":
        upload_compliance.subcommand(args, api)
    else:
        print(
            f"'{args.action}' is not a valid subcommand for airgap",
            file=sys.stderr,
        )
        sys.exit(1)
