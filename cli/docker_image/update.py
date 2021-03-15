#!/usr/bin/env python3

"""This module contain a update subcommand for the docker-image resource."""

from .utils import docker_image_update_params_from_args

def configure_parser(docker_image_subparser):
    """Adds the parser for the update command to an argparse ArgumentParser"""
    docker_image_update = docker_image_subparser.add_parser(
        "update", help="Update a docker image"
    )
    docker_image_update.add_argument(
        "--name", type=str, help="Edit the image name of the docker image"
    )
    docker_image_update.add_argument(
        "--tag", type=str, help="Edit the image tag of the docker image"
    )
    docker_image_update.add_argument(
        "--registry-id",
        type=str,
        help="Edit the registry id of the docker image",
    )
    docker_image_update.add_argument(
        "--engine-id", type=str, help="Edit the engine id of the docker image"
    )
    docker_image_update.add_argument(
        "--node-id", type=str, help="Edit the node of the docker image"
    )
    docker_image_update.add_argument("docker_image_id")


def subcommand(args, api):
    """Execute the update command with args."""
    params = docker_image_update_params_from_args(params={}, args=args)
    api.update_docker_image(args.docker_image_id, params=params)
