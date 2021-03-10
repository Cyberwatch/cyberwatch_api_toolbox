#!/usr/bin/env python3

import time
from dateutil import parser as datetime_parser
from datetime import datetime, timedelta


def configure_parser(docker_image_subparser):
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
    server = api.docker_image(args.docker_image_id)
    server_id = str(server[6])
    api.server_refresh(server_id)

    if args.wait:
        start_time = datetime.now()
        while not is_timeout(start_time, timeout=args.timeout):
            if analysis_is_finished(server_id, api, start_time):
                return
            time.sleep(2)
        raise TimeoutError("Timeout while waiting for the scan to finish")


def is_timeout(last_time, timeout):
    time = datetime.now()
    timeout_delta = timedelta(seconds=timeout)
    return (time - last_time) > timeout_delta


def get_last_server_analysis(server_id, api):
    server = api.server(server_id)
    return datetime_parser.parse(server.analyzed_at)


def analysis_is_finished(server_id, api, start_time):
    last_analysis = get_last_server_analysis(server_id, api)
    last_analysis = last_analysis.replace(tzinfo=None)
    return last_analysis > start_time
