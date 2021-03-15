#!/usr/bin/env python3

"""This module contain a create subcommand for the docker-image resource."""

import sys
import xml.etree.ElementTree as ET

def configure_parser(docker_image_subparser):
    """Adds the parser for the show command to an argparse ArgumentParser"""
    docker_image_show = docker_image_subparser.add_parser(
        "show", help="Show informations about a docker image"
    )
    docker_image_show_subparser = docker_image_show.add_subparsers(
        dest="information", help="Information to show"
    )
    docker_image_show_subparser.required = True

    init_show_vulnerabilities_subcommand(docker_image_show_subparser)


def subcommand(args, api):
    """Execute the show command with args."""
    if args.information == "vulnerabilities":
        vulnerabilities_subcommand(args, api)
    else:
        print(
            f"'{args.information}' is not a valid information to show.",
            file=sys.stderr,
        )
        sys.exit(1)


# Vulnerabilities


def init_show_vulnerabilities_subcommand(docker_image_show_subparser):
    """Adds the parser for the vulnerabilities subcommand to an argparse
    ArgumentParser"""
    docker_image_show_vulnerabilities_parser = (
        docker_image_show_subparser.add_parser(
            "vulnerabilities",
            help="Show vulnerabilities about a scanned docker image",
        )
    )
    docker_image_show_vulnerabilities_parser.add_argument("docker_image_id")
    docker_image_show_vulnerabilities_parser.add_argument(
        "--format",
        default="text",
        help="Format supported are 'junit-xml' and 'text'.",
    )


def vulnerabilities_subcommand(args, api):
    """Execute the vulnerabilities command with args."""
    docker_image = api.docker_image(args.docker_image_id)
    if docker_image is None:
        print(
            (
                f"No docker image with id={args.docker_image_id} "
                "has been found on Cyberwatch's instance."
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    server_id = str(docker_image[6])
    server = api.server(server_id)

    cve_announcements = []
    vulnerabilities = server.cve_announcements
    for vulnerability in vulnerabilities:
        cve_code = vulnerability.cve_code
        cve_announcements.append(api.cve_announcement(cve_code))
    generate_output(cve_announcements, docker_image, args, api)

    if vulnerabilities:
        sys.exit(1)


def generate_output(cve_announcements, docker_image, args, api):
    """Outputs CVE to stdout. Multiple formats are supported."""
    if args.format == "text":
        generate_text_output(cve_announcements)
    elif args.format == "junit-xml":
        generate_junit_xml_output(cve_announcements, docker_image, api)
    else:
        print(
            f"The following format is not supported: '{args.format}'.",
            file=sys.stderr,
        )
        sys.exit(1)


def generate_text_output(cve_announcements):
    """Outputs CVE to stdout as text"""
    cve_announcement_format_string = "{cve_code:14} {score:<5} {technologies}"
    print(
        cve_announcement_format_string.format(
            cve_code="CVE", score="SCORE", technologies="TECHNOLOGIES"
        )
    )
    for cve_announcement in cve_announcements:
        print(
            cve_announcement_format_string.format(
                cve_code=cve_announcement.cve_code,
                score=cve_announcement.score,
                technologies=",".join(
                    f"{techno.vendor}:{techno.product}"
                    for techno in cve_announcement.technologies
                ),
            )
        )


def generate_junit_xml_output(cve_announcements, docker_image, api):
    """Outputs CVE to stdout as junit xml"""
    testsuite = ET.Element(
        "testsuite", name="Vulnerabilities for docker image"
    )
    for cve_announcement in cve_announcements:
        technos = ",".join(
            f"{techno.vendor}:{techno.product}"
            for techno in cve_announcement.technologies
        )
        testcase = ET.SubElement(
            testsuite,
            "testcase",
            classname=f"{docker_image[1]}:{docker_image[2]}",
            name=(
                f"Vulnerability {cve_announcement.cve_code} "
                f"has been detected on technologies {technos} "
                f"with a score of {cve_announcement.score}"
            ),
            file=cve_announcement.cve_code,
            time="0.0",
        )
        failure = ET.SubElement(
            testcase, "failure", message="A vulnerability has been found."
        )
        failure.text = prettify_cve_announcement(cve_announcement, api.api_url)
    print(ET.tostring(testsuite).decode())


def prettify_cve_announcement(cve_announcement, api_url):
    """Format a cve_announcement to be human friendly."""
    return (
        f"[{cve_announcement.cve_code}] {cve_announcement.content}\n"
        f"Score: {cve_announcement.score}\n"
        f"Exploit code maturity: {cve_announcement.exploit_code_maturity}\n"
        f"Link: {api_url}/cve_announcements/{cve_announcement.cve_code}\n"
    )
