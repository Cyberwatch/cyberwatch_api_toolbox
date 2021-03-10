#!/usr/bin/env python3


def configure_parser(docker_image_subparser):
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
    params = docker_image_update_params_from_args(params={}, args=args)
    api.update_docker_image(args.docker_image_id, params=params)


def docker_image_update_params_from_args(params, args):
    if args.name:
        params["image_name"] = args.name
    if args.tag:
        params["image_tag"] = args.tag
    if args.registry_id:
        params["docker_registry_id"] = args.registry_id
    if args.engine_id:
        params["docker_engine_id"] = args.engine_id
    if args.node_id:
        params["docker_node_id"] = args.node_id
    return params
