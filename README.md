# Cyberwatch API toolbox

A simple interface for your Cyberwatch instance API.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Cyberwatch API toolbox](#cyberwatch-api-toolbox)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Install the package](#install-the-package)
    - [Test your installation](#test-your-installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [API Documentation](#api-documentation)
  - [Library Documentation](#library-documentation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

### Prerequisites
- [ ] [Python 3](https://www.python.org/)
- [ ] Python [PIP](https://pypi.org/project/pip/)

### Install the latest package

To install Cyberwatch API toolbox, simply use python 3 with:

```bash
$ pip3 install cbw-api-toolbox
```

### Install an older package version

Some scripts from version 1.X may not work in version 2.X of `cbw-api-toolbox`, to install an older version, simply do:

```bash
pip3 install cbw-api-toolbox==1.1.2
```

### Test your installation

**Create a new file called `ping.py` and copy/paste this content**

```python
# ping.py
import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()
```

**Configure an api.conf file with your credentials**

See the [Configuration](#configuration) section

**Test your script**

```bash
$ python3 ping.py
```

If everything is ok, the `OK` message will appear

```bash
$ python3 ping.py
INFO:root:OK
```

Otherwise, the `FAILED` message will appear

```
$ python3 ping.py
ERROR:root:FAILED
```

In this case, please check that there are no typing errors in your `API_KEY`, `SECRET_KEY` or `API_URL` and that your Cyberwatch instance is up.

## Configuration

Create an `api.conf` file at the root of the project (see `example_api.conf`)

- `api_key`: your Cyberwatch user api key
- `secret_key`: your Cyberwatch user secret key
- `url`: your Cyberwatch instance URL

**Example**

```conf
[cyberwatch]
api_key = PyXpxrcJ7rQ...
secret_key = +bUx37WnB0qt...
url = https://myinstance.local
```

To find your API credentials:
  1. Click on your profile page in your cyberwatch instance web page
  2. Click on the button 'see my api keys'

## Usage

**Launch a script example**

1. Choose a script from the [examples directory](examples) and copy it to your computer
2. Edit the script with your API credentials (See [Configuration](#configuration))
3. Launch the script

```bash
$ python3 your_example_script_file.py
```

## API Documentation

See the full API documentation [here](https://docs.cyberwatch.fr/api/#introduction)

## Library Documentation

See the library-specific documentation [here](./documentation.md)
