### Process to push a new version on PyPi (Python Package Index) with Github Actions

## Setup the package version

Edit the file `setup.py` to declare the new version:

```python
setup(
    ...
    version='2.0.1',
    ...
)
```

Commit the change, push to your Git repository remote on GitHub, create a pull request into the `master` branch.
Once the pull request is merged, the final steps are:

- Create a new release with the same version at https://github.com/Cyberwatch/cyberwatch_api_toolbox/releases
- Once created, a Github Action workflow will launch and upload the new version to PyPI

