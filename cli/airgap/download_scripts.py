#!/usr/bin/env python3

"""This module contain a "download-scripts" subcommand for the airgap
resource."""

import os
from itertools import groupby
from os.path import abspath, basename, dirname, join

import requests

from cbw_api_toolbox.cbw_api import CBWApi

SH_EXECUTE_SCRIPT = """#!/bin/bash
set -eu

readonly DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" &> /dev/null && pwd )"

for script in {}; do
    script=$DIR/$script
    chmod +x "$script"
    >&2 printf "Executing %s..." "$script"
    ( "$script" || >&2 echo "Error" ; ) && >&2 echo "Done"
done
"""


def configure_parser(airgap_subparser):
    """Adds the parser for the "download-scripts" command to an argparse
    ArgumentParser"""
    airgap_download_scripts = airgap_subparser.add_parser(
        "download-scripts", help="Download some airgap scripts"
    )
    airgap_download_scripts.add_argument(
        "--no-attachment", default=False, action="store_true"
    )
    airgap_download_scripts.add_argument("--dest-dir", default="cyberwatch-airgap")


def subcommand(args, api: CBWApi):
    """Execute the "download" command with args."""

    script_dir = join(abspath(args.dest_dir), "scripts")
    os.makedirs(script_dir, exist_ok=True)

    upload_dir = join(abspath(args.dest_dir), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    airgap_scripts_list = api.fetch_airgapped_scripts()
    script_os_association = groupby(
        sorted(
            download_individual_script(
                script_object,
                script_dir,
                api,
                with_attachment=not args.no_attachment,
            )
            for script_object in airgap_scripts_list
        ),
        lambda x: x[0],
    )

    create_run_scripts(script_os_association, base_directory=script_dir)
    print("INFO: Script saved in {}".format(script_dir))


def download_individual_script(
    script_object, base_directory, api: CBWApi, with_attachment=False
):
    """Get each script and put it in the correct category"""
    script = api.fetch_airgapped_script(str(script_object.id), params={"pristine": "1"})
    if script is None or script.type is None:
        return None, None

    target_os, script_name = script.type.split("::")[1:]
    script_filename = join(base_directory, "/".join((target_os, script_name)))
    os.makedirs(dirname(script_filename), exist_ok=True)
    script_filename = append_extension(script_filename)

    with open(script_filename, "w") as filestream:
        filestream.write(script.contents)

    if script.attachment and with_attachment:
        download_attachment(directory=dirname(script_filename), url=script.attachment)

    return target_os, basename(script_filename)


def download_attachment(directory, url):
    """Download attachment"""
    attachment = requests.get(url, allow_redirects=True, verify=False)
    attachment_filename = join(directory, basename(url))
    with open(attachment_filename, "wb") as file:
        file.write(attachment.content)


def append_extension(script_filename):
    """Append ".sh" or ".ps1" extension according to the OS"""
    os_target = script_filename.split("/")[-2]
    if os_target in ("Aix", "Linux", "Macos", "Vmware"):
        return f"{script_filename}.sh"
    if os_target == "Windows":
        return f"{script_filename}.ps1"
    return script_filename


def create_run_scripts(script_os_association, base_directory):
    """Create the run script according to the operating system in
    subdirectories"""
    for os_target, scripts in script_os_association:
        target_dir = join(base_directory, os_target)
        if os_target in ("Aix", "Linux", "Macos", "Vmware"):
            add_sh_run_script(scripts, target_dir)
        if os_target == "Windows":
            add_pwsh_run_script(scripts, target_dir)


def add_sh_run_script(os_and_scripts, directory):
    """Create a shell run script in directory"""
    run_script = join(directory, "run")
    with open(run_script, "w") as file_stream:
        file_stream.write(
            SH_EXECUTE_SCRIPT.format(" ".join(script for (_, script) in os_and_scripts))
        )
        os.chmod(run_script, 0o755)


def add_pwsh_run_script(os_and_scripts, directory):
    """Creates a "windows launch all" powershell script"""
    run_script_filename = join(directory, "run.ps1")
    with open(run_script_filename, "w") as file_stream:
        file_stream.write("$ScriptDir = Split-Path $MyInvocation.MyCommand.Path\n")
        for _, script in os_and_scripts:
            file_stream.write(f'& "$ScriptDir/{script}"\n')
