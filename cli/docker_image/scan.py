#!/usr/bin/env python3

"""This module contain a scan subcommand for the docker-image resource."""

import sys
import time
from datetime import datetime, timedelta

from dateutil.parser import parse

def configure_parser(docker_image_subparser):
    """Adds the parser for the scan command to an argparse ArgumentParser"""
    docker_image_scan = docker_image_subparser.add_parser(
        "scan", help="Scan a docker image"
    )
    docker_image_scan.add_argument(
        "--wait",
        action="store_true",
        help="Wait for the scan to finish before returning",
    )
    docker_image_scan.add_argument(
        "--timeout",
        type=int,
        default=300,
        help=(
            "Duration in second to wait for the scan "
            "to finish before failing"
        ),
    )
    docker_image_scan.add_argument("docker_image_id")


def subcommand(args, api):
    """Execute the scan command with args."""
    server = api.docker_image(args.docker_image_id)
    if server is None:
        print(
            (
                f"No docker image with id={args.docker_image_id} "
                "has been found on Cyberwatch's instance."
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    server_id = str(server[6])
    api.server_refresh(server_id)

    if args.wait:
        start_time = datetime.now()
        while not is_timeout(start_time, timeout=args.timeout):
            if analysis_is_finished(server_id, api, start_time):
                return
            time.sleep(2)
        raise TimeoutError("Timeout while waiting for the scan to finish")


def is_timeout(last_timestamp, timeout):
    """Return whether duration since last_timestamps is greater than timeout"""
    timestamp_now = datetime.now()
    timeout_delta = timedelta(seconds=timeout)
    return (timestamp_now - last_timestamp) > timeout_delta


def get_last_server_analysis(server_id, api):
    """Fetch the last time the server (i.e docker image) was analysed"""
    server = api.server(server_id)
    return parse(server.analyzed_at)


def analysis_is_finished(server_id, api, start_time):
    """Return whether the last analysis is newer than the start of the
    command"""
    last_analysis = get_last_server_analysis(server_id, api)
    last_analysis = last_analysis.replace(tzinfo=None)
    return last_analysis > start_time
