# Cyberwatch command line documentation

Cyberwatch's `cyberwatch-cli` command is Cyberwatch's command line interface. It
allows you to interact with the API of your local instance, such as managing and
scanning docker images.

## Install `cyberwatch-cli`

The command line is installed as part of the [the classic installation
process](../README.md#Installation).

## The syntax of `cyberwatch-cli`

The `cyberwatch-cli` command uses the following syntax:

```
cyberwatch-cli [RESOURCE] [ACTION]
```

To discover the syntax of the `cyberwatch-cli` command, you can use the `-h` flag

```sh
cyberwatch-cli -h
```

## Pass the configuration variables

The `cyberwatch-cli` command needs the variables `api-url`, `api-key` and
`secret-key` to work properly. Several ways of transmitting these variables are
supported.

### Through the command line

The syntax to pass the variables through the command line is:

```sh
cyberwatch-cli  --api-url https://myinstance.local \
                --api-key "PyXpxrcJ7rQ..."  \
                --secret-key "+bUx37WnB0qt..." \
                [RESOURCE] [ACTION]
```

### Through environnement variables

The variables can be set as environnement variables. You can use `API_URL`,
`API_KEY` and `SECRET_KEY`.

## Manage docker images

The `cyberwatch-cli` command provide actions `create`, `update` and `scan` to
interact with `docker-image` resources.

### Create a docker image

The recommended way to create a docker image is to duplicate an image already
present on the Cyberwatch instance and specify only what changes.

To create an image from an existing image whose `id` is 4, and change the `tag`
to `latest`, just run:

```sh
cyberwatch-cli docker-image create --from-image 4 --tag latest
```

### Update a docker image

To modify a docker image whose `id` is 4, and change the image to `ubuntu:latest`:

```sh
cyberwatch-cli docker-image update 4 --name ubuntu --tag latest
```

### Scan a docker image

To scan a docker image whose `id` is 4:

```sh
cyberwatch-cli docker-image scan 4
```

You can use the `--wait` flag to ask the program to wait until the scan is
finished before exiting. This can be useful in continuous integration.
