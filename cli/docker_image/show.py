#!/usr/bin/env python3

import sys


def configure_parser(docker_image_subparser):
    docker_image_show = docker_image_subparser.add_parser(
        "show", help="Show informations about a docker image"
    )
    docker_image_show_subparser = docker_image_show.add_subparsers(
        dest="information", help="Information to show"
    )
    docker_image_show_subparser.required = True

    init_show_vulnerabilities_subcommand(docker_image_show_subparser)


def subcommand(args, api):
    if args.information == "vulnerabilities":
        vulnerabilities_subcommand(args, api)
    else:
        print(
            f"'{args.information}' is not a valid information to show.",
            file=sys.stderr,
        )
        exit(1)


# Vulnerabilities


def init_show_vulnerabilities_subcommand(docker_image_show_subparser):
    docker_image_show_vulnerabilities_parser = (
        docker_image_show_subparser.add_parser(
            "vulnerabilities",
            help="Show vulnerabilities about a scanned docker image",
        )
    )
    docker_image_show_vulnerabilities_parser.add_argument("docker_image_id")


def vulnerabilities_subcommand(args, api):
    docker_image = api.docker_image(args.docker_image_id)
    if docker_image is None:
        print(
            (
                f"No docker image with id={args.docker_image_id} "
                "has been found on Cyberwatch's instance."
            ),
            file=sys.stderr,
        )
        exit(1)
    server_id = str(docker_image[6])
    server = api.server(server_id)

    vulnerabilities = server.cve_announcements
    CVE_ANNOUNCEMENT_FORMAT_STRING = "{cve_code:14} {score:<5} {technologies}"
    print(
        CVE_ANNOUNCEMENT_FORMAT_STRING.format(
            cve_code="CVE", score="SCORE", technologies="TECHNOLOGIES"
        )
    )
    for vulnerability in vulnerabilities:
        cve_code = vulnerability.cve_code
        cve_announcement = api.cve_announcement(cve_code)
        print(
            CVE_ANNOUNCEMENT_FORMAT_STRING.format(
                cve_code=cve_announcement.cve_code,
                score=cve_announcement.score,
                technologies=",".join(
                    f"{techno.vendor}:{techno.product}"
                    for techno in cve_announcement.technologies
                ),
            )
        )

    if vulnerabilities:
        print("Some vulnerabilities have been found")
        exit(1)
