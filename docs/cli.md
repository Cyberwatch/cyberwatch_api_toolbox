# Cyberwatch command line documentation

Cyberwatch's `cyberwatch-cli` command is Cyberwatch's command line interface. It
allows you to interact with the API of your local instance, such as managing and
scanning docker images.

## Install `cyberwatch-cli`

The command line is installed as part of the [the classic installation
process](../README.md#Installation).

## Use the Dockerfile

To use the api inside a docker container, you can use the Dockerfile. First,
build the image (here tagged as `cbw-api`), then you can run it with
environnement variables.

```sh
docker build . -t cbw-api
docker run --rm -e CBW_API_URL=https://myinstance.local \
                -e CBW_API_KEY="PyXpxrcJ7rQ..." \
                -e CBW_SECRET_KEY="+bUx37WnB0qt..." cbw-api
```

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

### List docker images

To list docker images present in the instance:

```sh
$ cyberwatch-cli docker-image list
ID  IMAGE:TAG                      NODE SERVER ENGINE REGISTRY
1   library/alpine:latest             1    431      2        1
2   library/ubuntu:latest             1    432      2        1
3   library/ubuntu:latest             1    433      2        1
4   library/node:12                   1    434      2        1
```

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

### Show informations about a docker image

#### Vulnerabilities

To show vulnerabilities associated to a docker image:

```
cyberwatch-cli docker-image show vulnerabilities
```

Several output format exists. The `junit-xml` output can be enabled with the
`--format` flag. The default format is `text`.

```
cyberwatch-cli docker-image show vulnerabilities --format junit-xml
```

Notice that a docker image must have been scanned before vulnerabilities can be
listed.

## Manage airgap assets

The command line interface can be used to download the scripts from the
Cyberwatch instance, and upload the results of these scripts.

### Download the scripts

To download the scripts to the default directory `scripts`:

```sh
cyberwatch-cli airgap download-scripts
```

By default, this command creates a tree structure similar to this one:

```
cyberwatch-airgap
├── scripts
│   ├── Aix
│   │   ├── InfoScript.sh
│   │   └── run
│   ├── Linux
│   │   ├── InfoScript.sh
│   │   ├── MetadataScript.sh
│   │   ├── PortsScript.sh
│   │   └── run
│   ├── Macos
│   │   ├── InfoScript.sh
│   │   └── run
│   ├── Vmware
│   │   ├── InfoScript.sh
│   │   └── run
│   └── Windows
│       ├── cbw_launch_all.ps1
│       ├── InfoScript.ps1
│       ├── MetadataScript.ps1
│       ├── PackagesScript.ps1
│       ├── PortsScript.ps1
│       └── WuaScript.ps1
└── uploads
```

The scripts downloaded from the Cyberwatch instance are stored in the `scripts` subfolder.

To specify a different destination directory:

```sh
export CYBERWATCH_DIR=/tmp/cyberwatch-airgap
cyberwatch-cli airgap download-scripts --dest-dir $CYBERWATCH_DIR
```

### Execute the scripts

To execute the scripts on a linux machine:

```sh
./cyberwatch-airgap/scripts/Linux/run > "cyberwatch-airgap/uploads/$(hostname)"
```

You can also copy the `cyberwatch-airgap/scripts/Linux` directory to an other
machine and execute the script on it.

To execute the scripts on a windows machine:

```powershell
.\cyberwatch-airgap\scripts\Windows\run.ps1 > .\cyberwatch-airgap\uploads\${env:COMPUTERNAME}
```

### Upload the results

To upload the results of the scripts:

```sh
cyberwatch-cli airgap upload
```

If no file are provided, the script tries to upload all the files present in
`cyberwatch-airgap/uploads` (relative to the current directory).

To provide manually the list of files to upload:

```sh
cyberwatch-cli airgap upload /tmp/cyberwatch-airgap/uploads/*
```
