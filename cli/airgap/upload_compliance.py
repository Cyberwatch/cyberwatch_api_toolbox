#!/usr/bin/env python3

"""This module contain a "upload-compliance" subcommand for the airgap resource."""

import os
import sys
import chardet

from cbw_api_toolbox.cbw_api import CBWApi


def configure_parser(airgap_script_subparser):
    """Adds the parser for the "upload-compliance" command to an argparse ArgumentParser"""
    airgap_script_upload = airgap_script_subparser.add_parser(
        "upload-compliance", help="Upload some compliance airgap result of scripts"
    )
    airgap_script_upload.add_argument("files", nargs="*", help="Files to upload")


def subcommand(args, api: CBWApi):
    """Execute the "upload-compliance" command with args."""
    files = args.files
    if not args.files:
        if not "cyberwatch-airgap-compliance" in os.listdir("."):
            print(
                "You need to provide a list of files to upload. "
                "The default is to upload all files present in "
                "a folder named 'cyberwatch-airgap-compliance/uploads' in your current directory."
            )
            sys.exit(1)

        files = (
            os.path.join(os.getcwd(), "cyberwatch-airgap-compliance", "uploads", name)
            for name in os.listdir("cyberwatch-airgap-compliance/uploads")
        )
    for script_result in files:
        upload_file(script_result, api)


def upload_file(result_script_filename, api: CBWApi):
    """Upload the `result_script_filename` to the Cyberwatch instance"""
    file_content = read_file_all_encodings(result_script_filename)
    json_content = {"output": file_content}
    print(f"INFO: Sending {result_script_filename} content to the API...")
    api.upload_compliance_airgapped_results(json_content)


def read_file_all_encodings(filename):
    """Return the content of `filename`. Detects the encoding used by the
    file."""
    with open(filename, "rb") as file_stream:
        raw_content = file_stream.read()
    detection = chardet.detect(raw_content)
    return raw_content.decode(detection["encoding"])
