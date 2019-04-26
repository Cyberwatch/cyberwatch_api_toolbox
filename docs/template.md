# Cyberwatch API Toolbox documentation

## Available methods

#### Ping

Sends a GET request to `/api/v2/ping` to validate that the API is working.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).ping()
INFO:root:OK
True
```

#### Servers

Sends a GET request to `/api/v2/servers` to retrieve the list of all servers.

#### Server
...

#### ....



## Available objects and their attributes

#### Server

| Attribute     | Type          | Description               | Exemple of possible value        |
|---------------|---------------|---------------------------|----------------------------------|
| id            | String (hash) | Unique id of the computer | 4a78524087574c12453dea248a91cadb |
| hostname      | String        | Hostname of the computer  | DESKTOP-AAA111                   |
| boot_at       | Date          | Date of the computer boot | 2016-05-30T09:54:58.000+02:00    |
| ...           | ...           | ...                       | ...                              |


#### RemoteAccess

...
