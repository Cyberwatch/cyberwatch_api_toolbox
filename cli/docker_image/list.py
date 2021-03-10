#!/usr/bin/env python3


def configure_parser(docker_image_subparser):
    docker_image_subparser.add_parser(
        "list", help="List docker images present on instance"
    )


def subcommand(args, api):
    images = api.docker_images()
    DOCKER_IMAGE_FORMAT_STRING = (
        "{id:<3} "
        "{image:30.30} "
        "{node_id:<4} "
        "{server_id:<6} "
        "{docker_engine_id:<6} "
        "{docker_registry_id:<8}"
    )
    print(
        DOCKER_IMAGE_FORMAT_STRING.format(
            id="ID",
            image="IMAGE:TAG",
            node_id="NODE",
            server_id="SERVER",
            docker_engine_id="ENGINE",
            docker_registry_id="REGISTRY",
        )
    )
    for image in images:
        print(
            DOCKER_IMAGE_FORMAT_STRING.format(
                id=image.id,
                image=f"{image.image_name}:{image.image_tag}",
                node_id=image.node_id,
                server_id=image.server_id,
                docker_engine_id=image.docker_engine_id,
                docker_registry_id=image.docker_registry_id,
            )
        )
