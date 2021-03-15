#!/usr/bin/env python3

"""This module contains functions used in other docker-image modules."""

def docker_image_update_params_from_args(params, args):
    """Update the `params` dictionnary from `args`."""
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
