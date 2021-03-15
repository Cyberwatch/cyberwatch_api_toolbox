#!/usr/bin/env python3

"""This module contain a create subcommand for the docker-image resource."""

from .utils import docker_image_update_params_from_args

def configure_parser(docker_image_subparser):
    """Adds the parser for the create command to an argparse ArgumentParser"""
    docker_image_create = docker_image_subparser.add_parser(
        "create", help="Create a docker image"
    )
    docker_image_create.add_argument(
        "--from-image",
        type=int,
        help="The image id from with the new docker image will be created",
    )
    docker_image_create.add_argument(
        "--name", type=str, help="Set the image name of the docker image"
    )
    docker_image_create.add_argument(
        "--tag", type=str, help="Set the image tag of the docker image"
    )
    docker_image_create.add_argument(
        "--registry-id",
        type=str,
        help="Set the registry id of the docker image",
    )
    docker_image_create.add_argument(
        "--engine-id", type=str, help="Set the engine id of the docker image"
    )
    docker_image_create.add_argument(
        "--node-id", type=str, help="Set the node of the docker image"
    )


IMAGE_FIELDS = [
    "docker_image_id",
    "image_name",
    "image_tag",
    "docker_registry_id",
    "docker_engine_id",
    "node_id",
    "server_id",
]


def subcommand(args, api):
    """Execute the create command with args."""
    params = {}
    if args.from_image:
        from_image = api.docker_image(str(args.from_image))
        for key, value in zip(IMAGE_FIELDS, from_image):
            params[key] = value
    params = docker_image_update_params_from_args(params, args)
    result = api.create_docker_image(params=params)
    print(result.id)
