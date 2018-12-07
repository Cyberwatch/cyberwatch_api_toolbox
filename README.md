# Cyberwatch API toolbox

A simple interface with your Cyberwatch instance API :

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

To install Cyberwatch API toolbox, simply use python 3 with :

``` {.sourceCode .bash}
$ pip3 install git+https://github.com/Cyberwatch/cyberwatch_api_toolbox
```

Usage
------------

- To launch a script example :
    - Install the package (see above)
    - And then copy the example on your computer from the [examples directory](examples)

- To use this example you will need to edit the script as follow : 
    - Enter your cyberwatch instance url in ```YOUR_API_URL```
    
    *Example : YOUR_API_URL = 'https://myinstance.local'*
    
    - Enter your cyberwatch user api key in ```YOUR_CBW_API_KEY```
    
    *Example : YOUR_CBW_API_KEY = 'PyXpxrcJ7rQ...'*
    
    - Enter your cyberwatch user api secret in ```YOUR_CBW_SECRET_KEY```
    
    *Example : YOUR_CBW_SECRET_KEY = '+bUx37WnB0qt...'*

- To find your api key and api secret key :
    - Click on your profile page in your cyberwatch instance web page
    - Click on the button 'see my api keys'
    
Finally to start the script : 
``` {.sourceCode .python}
$ python3 your_example_script_file.py
```
