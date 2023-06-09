#!/usr/bin/env python3

"""This module contain a "download-compliance-scripts" subcommand for the airgap
resource."""

import os
import sys
import shutil
from os.path import abspath, dirname, join

from cbw_api_toolbox.cbw_api import CBWApi
from cli.os.list_os import subcommand as list_os

def configure_parser(airgap_subparser):
    """Adds the parser for the "download-compliance-scripts" command to an argparse
    ArgumentParser"""
    airgap_download_scripts = airgap_subparser.add_parser(
        "download-compliance-scripts", help="Download some compliance airgap scripts"
    )
    airgap_download_scripts.add_argument(
        "--list-os",
        action="store_true",
        help="List available Operating systems. Overrides other options.")
    airgap_download_scripts.add_argument("--os")
    airgap_download_scripts.add_argument(
        "--repositories", "--groups", nargs='+',
        help='Repositories to fetch, ex : "-- repositories CIS_Benchmark Cyberwatch"')
    airgap_download_scripts.add_argument(
        "--dest-dir", default="cyberwatch-airgap-compliance")


def subcommand(args, api: CBWApi):
    """Execute the "download" command with args."""

    if args.list_os:
        list_os(api)
        return

    if args.os is None or args.repositories is None:
        print("Error: the following arguments are required: --os, --repositories/--groups")
        sys.exit(1)

    script_dir = join(abspath(args.dest_dir), "scripts")
    if os.path.exists(script_dir):
        shutil.rmtree(script_dir)
    os.makedirs(script_dir)

    upload_dir = join(abspath(args.dest_dir), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    airgap_scripts_list = api.fetch_compliance_airgapped_scripts(
        {"os": args.os, "repositories": args.repositories})
    if not airgap_scripts_list:
        print("No scripts downloaded with matching criteria")
        sys.exit(0)
    os_target = download_individual_script(airgap_scripts_list, script_dir)
    print("INFO: Script saved in {}".format(script_dir))


def download_individual_script(script_object, base_directory):
    """Get each script and put it in the correct category"""
    script_filename = "".join((base_directory, "/", script_object[0]))

    os.makedirs(dirname(script_filename), exist_ok=True)
    with open(script_filename, "w") as filestream:
        filestream.write(script_object[1])
