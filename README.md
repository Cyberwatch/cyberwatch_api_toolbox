# Cyberwatch API toolbox

A simple interface with your Cyberwatch instance API:

``` {.sourceCode .python}
>>> from cbw_api_toolbox.cbw_api import CBWApi
>>> api = CBWApi(YOUR_API_URL, YOUR_CBW_API_KEY, YOUR_CBW_SECRET_KEY)
>>> servers = api.servers()
>>> servers[0].cve_announcements_count
153
```

Installation
------------

**Prerequisite**
- [Python 3](https://www.python.org/)
- Python [PIP](https://pypi.org/project/pip/)

To install Cyberwatch API toolbox, simply use python 3 with:

``` {.sourceCode .bash}
$ pip3 install git+https://github.com/Cyberwatch/cyberwatch_api_toolbox
```

Test your installation
------------
- Install the package (see above)
- Configure the test script : 
    - Create a new file called ```ping.py```
    - Copy and paste : 
    ``` {.sourceCode .python}
    from cbw_api_toolbox.cbw_api import CBWApi
    
    API_KEY = ''
    SECRET_KEY = ''
    API_URL = ''
    
    CBWApi(API_URL, API_KEY, SECRET_KEY).ping()
    ```
    - Edit this script with **Configure** below.
    - Launch the script with `python3 ping.py`
    - You should see `OK`, if you have a `Failed` you should review your configuration.

Configure
------------
- Enter your cyberwatch user api key in ```API_KEY```
    
*Example: API_KEY = 'PyXpxrcJ7rQ...'*

- Enter your cyberwatch user api secret in ```SECRET_KEY```

*Example: SECRET_KEY = '+bUx37WnB0qt...'*

- Enter your cyberwatch instance url in ```API_URL```

*Example: API_URL = 'https://myinstance.local'*

- To find your api key and api secret key:
    - Click on your profile page in your cyberwatch instance web page
    - Click on the button 'see my api keys'

Usage
------------

- To launch a script example:
    - Install the package (see above)
    - And then choose and copy an example to your computer from the [examples directory](examples)

- To use this example you will need to **edit** the script with your configuration (see **Configure**)     

- After this steps your file should look like : 
``` {.sourceCode .python}
from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = 'PyXpxrcJ7rQ...'
SECRET_KEY = '+bUx37WnB0qt...'
API_URL = 'https://myinstance.local'

servers = CBWApi(API_URL, API_KEY, SECRET_KEY).get_detailed_servers()
```

Finally to start the script: 
``` {.sourceCode .python}
$ python3 your_example_script_file.py
```


