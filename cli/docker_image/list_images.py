#!/usr/bin/env python3

"""This module contain a list subcommand for the docker-image resource."""

def configure_parser(docker_image_subparser):
    """Adds the parser for the list command to an argparse ArgumentParser"""
    docker_image_subparser.add_parser(
        "list", help="List docker images present on instance"
    )


def subcommand(api):
    """Execute the list command with args."""
    images = api.docker_images()
    docker_image_format_string = (
        "{id:<3} "
        "{image:30.30} "
        "{node_id:<4} "
        "{server_id:<6} "
        "{docker_engine_id:<6} "
        "{docker_registry_id:<8}"
    )
    print(
        docker_image_format_string.format(
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
            docker_image_format_string.format(
                id=image.id,
                image=f"{image.image_name}:{image.image_tag}",
                node_id=image.node_id,
                server_id=image.server_id,
                docker_engine_id=image.docker_engine_id,
                docker_registry_id=image.docker_registry_id,
            )
        )
