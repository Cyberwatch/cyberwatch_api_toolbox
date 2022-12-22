from setuptools import setup, find_packages

setup(
    name='cbw-api-toolbox',
    description='CyberWatch Api Tools.',
    long_description=open('README.md').read().strip(),
    long_description_content_type="text/markdown",
    version='2.3.1',
    author='CyberWatch SAS',
    author_email='support-it+api@cyberwatch.fr',
    license='MIT',
    url='https://github.com/Cyberwatch/cyberwatch_api_toolbox',
    project_urls={
        "Documentation": "https://docs.cyberwatch.fr/api/#introduction",
    },
    py_modules=['cbw-api-toolbox'],
    zip_safe=False,
    packages=find_packages(),
    package_dir={'cbw_api_toolbox': 'cbw_api_toolbox'},
    install_requires=[
        "requests>=2.20.1",
        "XlsxWriter>=1.2.1",
        "openpyxl>=3.0.6",
        "python-dateutil>=2.8.1",
        "chardet>=3.0.4"
    ],
    scripts=['bin/cyberwatch-cli']
)
