### Process to push a new version on PyPi (Python Package Index)

## Generating distribution archives

Make sure you have the latest versions of setuptools and wheel installed:

```sh
pip3 install --user --upgrade setuptools wheel
```

Now run this command to build the source archive (tar.gz) and the built distribution (.whl) :

```sh
python3 setup.py sdist bdist_wheel
```

The command should have generated 2 files in the `dist` folder:

```sh
dist/
  cyberwatch_api_toolbox-0.0.1-py3-none-any.whl
  cyberwatch_api_toolbox-0.0.1.tar.gz
```

## Setup API token

Create an `.pypirc` file at the root of the project (see `.example_pypirc`)

- `username`: `__token__`, specify the use of an API token for authentication
- `password`: the API token value, including the `pypi-` prefix (Please use the official key pair (Ask Cyberwatch management if needed))

Note: In case the keys are not accessible, please generate a new on at https://pypi.org/manage/account/#api-tokens

**Example**

```conf
[pypi]
username = __token__
password = password = pypi-AgEIcHlwaS5vcmcCJDhkNGQyNDBjLTZjMGEtND...
```

## Uploading the distribution archives

Use twine to upload the distribution packages:

```sh
pip3 install --user --upgrade twine
```

Once installed, run Twine to upload all of the archives under `dist`:

```sh
python3 -m twine upload --config-file .pypirc --repository pypi dist/*
```



