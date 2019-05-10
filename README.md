# Cyberwatch API toolbox

A simple interface for your Cyberwatch instance API.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install the package](#install-the-package)
  - [Test your installation](#test-your-installation)
- [Configuration](#configuration)
- [Usage](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

### Prerequisites
- [ ] [Python 3](https://www.python.org/)
- [ ] Python [PIP](https://pypi.org/project/pip/)

### Install the package

To install Cyberwatch API toolbox, simply use python 3 with:

```bash
$ pip3 install git+https://github.com/Cyberwatch/cyberwatch_api_toolbox
```

### Test your installation

**Create a new file called `ping.py` and copy/paste this content**

```python
# ping.py
from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CBWApi(API_URL, API_KEY, SECRET_KEY).ping()
```

**Configure the file with your credentials**

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

- `API_KEY`: your Cyberwatch user api key
- `SECRET_KEY`: your Cyberwatch user secret key
- `API_URL`: your Cyberwatch instance URL

**Example**

```python
API_KEY = 'PyXpxrcJ7rQ...'
SECRET_KEY = '+bUx37WnB0qt...'
API_URL = 'https://myinstance.local'
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

[Cyberwatch api documentation](./documentation.md)
