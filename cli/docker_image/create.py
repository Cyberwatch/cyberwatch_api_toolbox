#!/usr/bin/env python3


def configure_parser(docker_image_subparser):
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
    params = {}
    if args.from_image:
        from_image = api.docker_image(str(args.from_image))
        for key, value in zip(IMAGE_FIELDS, from_image):
            params[key] = value
    params = docker_image_update_params_from_args(params, args)
    result = api.create_docker_image(params=params)
    print(result.id)


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
