# Cyberwatch API Toolbox documentation

## Available methods

#### Ping

Send a GET request to `/api/v3/ping` to validate that the API is working.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).ping()
INFO:root:OK
True
```

#### Servers

Send a GET request to `/api/v3/servers` to retrieve the list of all servers.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).servers()
[<cbw_api_toolbox.cbw_objects.cbw_server.CBWServer ...]
```

#### Server

Send a GET request to `/api/v3/servers/{SERVER_ID}` to retrieve the information of a server.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).server(SERVER_ID)
[<cbw_api_toolbox.cbw_objects.cbw_server.CBWServer]
```

#### Update server

Send a PATCH request  `/api/v3/servers/{SERVER_ID}` to update the information of a server.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).update_server(SERVER_ID, INFO)
True
```

#### Delete server

Send a DELETE request `/api/v3/servers/{SERVER_ID}` to delete a server.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).delete_server(SERVER_ID)
True
```

#### Remote accesses

Send a GET request `/api/v3/remote_accesses` to retrieve the list of all remote accesses.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).remote_accesses()
[<cbw_api_toolbox.cbw_objects.cbw_remote_access.CBWRemoteAccess...]
```

#### Remote access

Send a GET request `/api/v3/remote_accesses/{REMOTE_ACCESS_ID}` to retrieve the information of a particular remote access.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).remote_access(REMOTE_ACCESS_ID)
[<cbw_api_toolbox.cbw_objects.cbw_remote_access.CBWRemoteAccess]
```

#### Create remote access

Send a POST request `/api/v3/remote_accesses` to create a remote access.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).create_remote_access(INFO)
INFO:root:remote access successfully created {ADDRESS}
True
```

#### Update remote access

Send a PATCH request `/api/v3/remote_accesses/{REMOTE_ACCESS_ID}` to update the information of a particular remote access.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).update_remote_access(REMOTE_ACCESS_ID, INFO)
True
```

#### Delete remote access

Send a DELETE request `/api/v3/remote_accesses/{REMOTE_ACCESS_ID}` to delete a remote access.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).delete_remote_access(REMOTE_ACCESS_ID)
True
```

#### Test an agentless deployment

Send a POST request `/api/v3/remote_accesses/{REMOTE_ACCESS_ID}/test_deploy` to test a remote access.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).test_deploy_remote_access(REMOTE_ACCESS_ID)
<cbw_api_toolbox.cbw_objects.cbw_remote_access.CBWRemoteAccess>
```

#### CVE Announcement

Send a GET request to `/api/v2/cve_announcements/{CVE_CODE}` to get all informations about a specific cve_announcement

###### Usage example and expected result:

```python
>>> CBWApi(API_URL, API_KEY, SECRET_KEY).cve_announcement(CVE_CODE)
[<cbw_api_toolbox.cbw_objects.cbw_cve.CBWCve]
```

#### Groups

Send a GET request to `/api/v3/groups` to get informations about all groups

###### Usage example and expected result:

```python
>>> CBWApi(API_URL, API_KEY, SECRET_KEY).groups()
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWGroup]
```

#### Group

Send a GET request `/api/v3/groups/{GROUP_ID}` to retrieve the information of a particular group.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).group(GROUP_ID)
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWGroup]
```

#### Create group

Send a POST request `/api/v3/groups` to create a group.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).create_group(INFO)
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWGroup]
```

#### Update group

Send a PUT request `/api/v3/groups/{GROUP_ID}` to update the information of a particular group.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).update_group(GROUP_ID, INFO)
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWGroup]
```

#### Delete group

Send a DELETE request `/api/v3/groups/{GROUP_ID}` to delete a group.

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).delete_group(GROUP_ID)
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWGroup]
```

#### User

Send a GET request to `/api/v3/users/<id>` to get informations about a specific user

###### Usage example and expected result:

```python
>>> CBWApi(API_URL, API_KEY, SECRET_KEY).users(USER_ID)
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWUsers]
```

#### Users

Send a GET request to `/api/v3/users` to get informations about all users

###### Usage example and expected result:

```python
>>> CBWApi(API_URL, API_KEY, SECRET_KEY).users()
[<cbw_api_toolbox.cbw_objects.cbw_group.CBWUsers]
```

#### Nodes

Send a GET request to `/api/v3/nodes` to retrieve a list of all nodes.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).nodes()
[<cbw_api_toolbox.cbw_objects.cbw_node.CBWNode ...]
```

#### Node

Send a GET request to `/api/v3/nodes/{NODE_ID}` to retrieve the information of a node.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).node(NODE_ID)
[<cbw_api_toolbox.cbw_objects.cbw_node.CBWNode]
```

#### Delete Node

Send a DELETE request to `/api/v3/nodes/{NODE_ID}` to delete a node and transfer the data to another one.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).node(NODE_ID, NEW_NODE_ID)
[<cbw_api_toolbox.cbw_objects.cbw_node.CBWNode]
```

#### Host

Send a GET request `/api/v3/hosts/{HOST_ID}` to retrieve the information of a particular host.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).host(HOST_ID)
[<cbw_api_toolbox.cbw_objects.cbw_host.CBWHost]
```

#### Hosts

Send a GET request `/api/v3/hosts` to retrieve all the hosts.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).hosts()
[<cbw_api_toolbox.cbw_objects.cbw_host.CBWHost]...]
```

#### Create host

Send a POST request `/api/v3/hosts` to create a host.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).create_host(INFO)
[<cbw_api_toolbox.cbw_objects.cbw_host.CBWHost]
```

#### Update host

Send a PUT request `/api/v3/hosts/{HOST_ID}` to update the information of a particular host.

###### Usage example and expected result:

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).update_host(HOST_ID, INFO)
[<cbw_api_toolbox.cbw_objects.cbw_host.CBWHost]
```

#### Delete host

Send a DELETE request `/api/v3/hosts/{HOST_ID}` to delete a host.

```python
>>> CBWApi(URL, API_KEY, SECRET_KEY).delete_host(HOST_ID)
[<cbw_api_toolbox.cbw_objects.cbw_host.CBWHost]
```

## Available objects and their attributes

### Server object

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| id                        | String (hash) | Unique id of the computer         | 4a78524087574c12453dea248a91cadb                  |
| applications              | Object        | List of the computer's applications|                                                  |
| boot_at                   | Date          | Date of the computer boot         | 2016-05-30T09:54:58.000+02:00                     |
| category                  | String        | Computer's category               | server                                            |
| created_at                | Date          | Date of the computer creation     | 2019-06-26T09:46:58.000+02:00
| criticality               | String        | Computer's criticality            | criticality_medium                                |
| cve_announcements         | Object        | List of CVEs affecting the computer| [Cve](#Cve)                                      |
| cve_announcements_count   | Int           | Number of CVEs                    | 3                                                 |    
| deploying_period          | Object        | Computer's deploying period       | [Deploying Period](#Deploying-period)             |
| description               | String        | Computer's description            | "production machine"                              |
| groups                    | Object        | Computer's groups                 | [Group](#Group)                                   |
| hostname                  | String        | Computer's hostname               | "XXX.XXX.XXX.XXX"                                 |
| ignoring_policy           | Object        | Computer's Ignoring policy        | [Ignoring Policy](#Ignoring-policy)               |
| last_communication        | Date          | Date of last communication with the computer| 2019-04-08T15:46:22.000+02:00           |
| os                        | Object        | Computer's OS                     | [Os](#Os)                                         |
| packages                  | Object        | List of the computer's packages   | [Package](#Package)                               |
| reboot_required           | Bool          | The computer requires to be rebooted| false                                           |
| remote_ip                 | String        | Computer's IP address             | XXX.XXX.XXX.XXX                                   |
| status                    | List          | Computer's status                 | comment: "Communication failure"                  |
| updates                   | Object        | Available updates for the computer| [Update](#Update)                                 |
| updates_count             | Int           | Number of available updates for the computer| 3                                       |
| compliance_groups         | Object        | Computer's compliance groups      | [Group](#Group)                                   |

### Group

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| id                        | Int           | id of the group                   | 140                                               |
| color                     | String (hex)  | Color to affect to the group      | "#12AFCB"                                         |
| name                      | String        | name of the group                 | "app_windows"                                     |
| description               | String        | Description of the group          | "main servers"                                    |

### Deploying period

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| autoplanning              | Bool          | Automatically generate update scripts for computers in the deploying period| false    |
| autoreboot                | Bool          | Automatically generate reboot scripts for computers in the deploying period| false    |
| end_time                  | String        | Deploying period end time         | "06:00"                                           |
| name                      | String        | Name of the deploying period      | "test"                                            |
| next_occurence            | String (date) | Next time frame occurence of the deploying period| "2019-04-27T00:00:00.000+02:00"    |
| start_time                | String        | Deploying period start time       | "00:00"                                           |

#### Os

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| arch                      | String        | OS architecture                   | "x86_64"                                          |
| created_at                | String (date) | Creation date in Cyberwatch       | "2019-04-08T11:01:20.000+02:00"                   |
| eol                       | String        | OS end of support as provided by their vendor| "2023-04-26T02:00:00.000+02:00"        |
| key                       | String        | OS key in Cyberwatch              | "ubuntu_1804_64"                                  |
| name                      | String        | OS name                           | "Ubuntu 18.04"                                    |
| short_name                | String        | OS short name                     | "Ubuntu 18.04"                                    |
| type                      | String        | OS type in Cyberwatch             | "Os::Ubuntu"                                      |
| updated_at                | String (date) | Last modification date in Cyberwatch| "2019-04-08T11:01:20.000+02:00"                 |

### Ignoring policy

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| ignoring_policy_items     | Object        | Items of the ignoring policy      | [Ignoring Policy Items](#Ignoring-policy-item)    |
| name                      | String        | Name of the ignoring policy       | "test_policy"                                     |

### Ignoring policy item

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| keyword                   | String        | Keyword of the packages           | "test"                                            |
| version                   | String        | Version of the packages           | "0.1"                                             |

### Package

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| hash_index                | String (hash) | Hash identifier                   | "0160e4a3d38518a2660ff61b89c1407df"               |
| product                   | String        | Name of the package               | "gpg-wks-server"                                  |
| type                      | String        | Package type in Cyberwatch        | "Packages::Deb"                                   |
| vendor                    | String        | Vendor of the package             | null                                              |
| version                   | String        | Package version                   | "2.2.4-1ubuntu1.2"                                |

#### Security announcement

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| created_at                | String (date) | Creation date in Cyberwatch       | "2019-04-08T02:00:00.000+02:00"                   |
| cve_code                  | String        | CVE Code                          | "CVE-2019-3842"                                   |
| link                      | String        | URL of the security announcement  | "https://usn.ubuntu.com/3938-1"                   |
| sa_code                   | String        | Security announcement code        | "USN-3938-1"                                      |
| type                      | String        | Security announcement type in Cyberwatch| "SecurityAnnouncements::Ubuntu"             |
| updated_at                | String (date) | Last modification date in Cyberwatch| "2019-04-10T09:20:07.000+02:00"                 |

#### Update

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| created_at                | String (date) | Creation date of the update in Cyberwatch| "2019-04-09T17:13:07.000+02:00"            |
| current                   | Object        | Vulnerable version of the package affected by the update| [Current](#Package)         |
| cve_announcements         | Object        | List of the CVEs concerned by the update| [Cve](#Cve)                                 |
| ignored                   | Bool          | Boolean checking whether if the update has been ignored or not| false                 |
| patchable                 | Bool          | Boolean checking whether if the update is patchable via Cyberwatch or not| true       |
| target                    | Object        | Version of the package to update to| [Target](#Package)                               |
| updated_at                | String (date) | Last modification date of the update in Cyberwatch| "2019-04-09T17:13:07.000+02:00"   |

### Cve

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| content                   | String        | CVE description                   | "In systemd before v242-r…her than \"allow_any\"."|
| created_at                | String (date) | Creation date of the CVE in Cyberwatch| "2019-04-08T22:17:34.000+02:00"               |
| cve_code                  | String        | CVE code                          | "CVE-2019-5953"                                   |
| cvss_v2                   | Object        | CVSS v2 metrics object               | [CVSS v2](#CVSS_v2)                            |
| cvss_v3                   | Object        | CVSS v3 metrics object               | [CVSS v3](#CVSS_v3)                            |
| level                     | String        | CVSS Score level                  | "level_medium"                                    |
| score                     | Float         | CVE score (CVSS v2 or v3, depends on options) | 4.4                                   |
| score_v2                  | Float         | CVE score from CVSS v2            | 4.4                                               |
| score_v3                  | Float         | CVE score from CVSS v3            | 4.4                                               |
| last_modified             | String        | Last modification date of the CVE by the authorities| "2019-04-26T16:45:22.000+02:00" |
| published                 | String        | Publication date of the CVE by the authorities| "2019-04-09T23:29:03.000+02:00"       |
| updated_at                | String (date) | Last modification date of the CVE in Cyberwatch| "2019-04-29T09:33:37.000+02:00"      |
| exploitable               | Boolean       | Boolean checking whether an exploit was found for this specific CVE| True             |
| servers                   | List          | List of affected servers and their attributes for this CVE|[{'active': True, 'comment': None, 'fixed_at': None, 'ignored': False, 'server': [Server](#Server)}] |

> **Note:** not every attributes of the server object is sent back, for example, the "updates" attribute only contains updates fixing the current CVE and not every available fixes for the server.

### Node object

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| id                        | String        | Node Id                           | 1                                                 |
| created_at                | String        | Creation date of the node         | "2019-04-08T02:00:00.000+02:00"                   |
| name                      | String        | Node name                         | "master"                                          |
| updated_at                | String        | Last modification of the node     | "2019-04-08T02:00:00.000+02:00"                   |

### User

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| email                     | String        | Email of user                     | "test@example.com"                                |
| firstname                 | String        | First name of user                | "Cyberwatch"                                      |
| id                        | Int           | User id                           | 25                                                |
| locale                    | String        | Locale of user                    | "fr"                                              |
| login                     | String        | Login email of user               | "test@example.com"                                |
| name                      | String        | Name of user                      | "Cyberwatch"                                      |
| server_groups             | Object        | Server Groups of user             | [server_groups](#Server-groups)                   |
| auth_provider             | String        | Authentification provider of user | "ldap"                                            |

### Server groups

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| id                        | Int           | Server group id                   | 25                                                |
| name                      | String        | Name of group                     | "Cyberwatch"                                      |
| role                      | String        | Role of server group              | "system_admin"                                    |

### Remote Access object

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| address                   | String        | Address of remote access          | "XXX.XXX.XXX.XXX"                                 |
| id                        | Int           | Remote access  id                 | 1                                                 |
| is_valid                  | Boolean       | Boolean checking whether if the remote acess is valid or not| false                   |
| node_id                   | Int           | Id of node of remote access       | 1                                                 |
| port                      | Int           | Port of remote access             | 22                                                |
| type                      | String        | Type of remote access             | "CbwRam::RemoteAccess::Ssh::WithPassword"         |
| last_error                | String        | Last error of remote access       | "Net::SSH::ConnectionTimeout"                     |
| server_id                 | Int           | Id of server linked to remote access| 73                                              |

### CVSS_v2 object

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| access_complexity         | String        | Access complexity of CVE          | "access_complexity_low"                           |
| access_vector             | String        | Access vector of CVE              | "access_vector_network"                           |
| availability_impact       | String        | Impact on availability of CVE     | "availability_impact_none"                        |
| confidentiality_impact    | String        | Impact on confidientiality of CVE | "confidentiality_impact_none"                     |
| integrity_impact          | String        | Impact on integrity of CVE        | "integrity_impact_high"                           |
| authentication            | String        | Authentication level required for CVE| "authentication_none"                          |

### CVSS_v3 object

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| access_complexity         | String        | Access complexity of CVE          | "access_complexity_low"                           |
| access_vector             | String        | Access vector of CVE              | "access_vector_network"                           |
| availability_impact       | String        | Impact on availability of CVE     | "availability_impact_none"                        |
| confidentiality_impact    | String        | Impact on confidientiality of CVE | "confidentiality_impact_none"                     |
| integrity_impact          | String        | Impact on integrity of CVE        | "integrity_impact_high"                           |
| privilege_required        | String        | Privilege level required for CVE  | "privilege_required_none"                         |
| scope                     | String        | Scope of the CVE                  | "scope_unchanged"                                 |
| user_interaction          | String        | User interaction level for CVE    | "user_interaction_none"                           |

### Host

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| id                        | String (hash) | Unique id of the host             | 4a78524087574c12453dea248a91cadb                  |
| technologies              | Object        | List of the host technologies     | [Technologies](#Package)                          |
| category                  | String        | Host category                     | server                                            |
| created_at                | Date          | Date of the host creation         | 2019-06-26T09:46:58.000+02:00                     |
| cve_announcements         | Object        | List of CVEs affecting the host   | [Cve](#Cve)                                       |
| cve_announcements_count   | Int           | Number of CVEs                    | 3                                                 |    
| hostname                  | String        | Host hostname                     | "XXX.XXX.XXX.XXX"                                 |
| target                    | String        | Host IP address                   | XXX.XXX.XXX.XXX                                   |
| security_issues           | Object        | List of the host security issues  |                                                   |
| status                    | List          | Host status                       | comment: "Communication failure"                  |
| scans                     | Object        | Scans of host                     |                                                   |
| server_id                 | Int           | Id of server linked to host       | 73                                                |
| node_id                   | Int           | Id of node of host                | 1                                                 |
| updated_at                | String        | Last modification of the host     | "2019-04-08T02:00:00.000+02:00"                   |

### Security issue

| Attribute                 | Type          | Description                       | Example of possible value                         |
|---------------------------|:-------------:|:---------------------------------:|---------------------------------------------------|
| id                        | String        | Unique id of the security issue   | 2                                                 |
| sid                       | String        | SID of the security issue         | Security_Issue_1                                  |
| description               | String        | Description of the security issue |  "security issue description"                     |
| level                     | String        | Severity of the security issue    | level_critical                                    |
| cve_announcements         | Object        | List of CVEs related to the SI    | [Cve](#Cve)                                       |
| servers                   | Object        |  List of servers related to the SI| [Server](#Server-object)                          |    
| score                     | Int           | Score of the security issue       | 8                                                 |
| title                     | String        | Title of the security issue       | "SEC_ISSUE 01"                                    |
| type                      | String        | Type of the security issue        | "SecurityIssues::Custom"                          |
