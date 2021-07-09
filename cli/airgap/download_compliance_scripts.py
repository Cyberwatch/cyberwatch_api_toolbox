#!/usr/bin/env python3

"""This module contain a "download-compliance-scripts" subcommand for the airgap
resource."""

import os
import sys
import shutil
from os.path import abspath, dirname, join

from cbw_api_toolbox.cbw_api import CBWApi
from cli.os.list_os import subcommand as list_os

SH_EXECUTE_SCRIPT = """#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

mkdir ${DIR}/../uploads

for script in ${DIR}/*.sh; do
  script_basename=$(basename $script)
  result_filename=$(hostname)_${script_basename%.*}
  bash "$script" > ${DIR}/../uploads/$result_filename 2>&1
done
"""

PS1_EXECUTE_SCRIPT = """
$hostname = [System.Net.Dns]::GetHostName()

If ( !( Test-Path -Path .\\..\\uploads )) { New-Item -ItemType Directory -Force -Path .\\..\\uploads | Out-Null }

Get-ChildItem -Path "$PSScriptRoot" -Filter "*.ps1" | ForEach-Object {
  If ($_.FullName -NotLike ("*" + $MyInvocation.MyCommand.Name + "*")) {
  Write-Host ("Current script: " + $_.FullName)
  & $_.FullName 2>&1 > $("$PSScriptRoot\\..\\uploads\\" + $hostname + "_" + $_.BaseName + ".txt")
  }
}
"""


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
    create_run_scripts(os_target, script_dir)
    print("INFO: Script saved in {}".format(script_dir))


def download_individual_script(script_object, base_directory):
    """Get each script and put it in the correct category"""
    for script in script_object:
        script_filename = "".join((base_directory, "/", script.filename))

        os.makedirs(dirname(script_filename), exist_ok=True)
        with open(script_filename, "w") as filestream:
            filestream.write(script.script_content)

    if ".ps1" in script_object[0].filename:
        os_target = "Windows"
    else:
        os_target = "Linux"

    return os_target


def create_run_scripts(os_target, base_directory):
    """Create the run script according to the operating system"""

    if os_target in "Windows":
        run_script = join(base_directory, "run.ps1")
        with open(run_script, "w") as file_stream:
            file_stream.write(PS1_EXECUTE_SCRIPT)
    else:
        run_script = join(base_directory, "run")
        with open(run_script, "w") as file_stream:
            file_stream.write(SH_EXECUTE_SCRIPT)
            os.chmod(run_script, 0o755)
