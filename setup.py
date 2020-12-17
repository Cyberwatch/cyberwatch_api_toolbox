from setuptools import setup

setup(
    name='cbw-api-toolbox',
    description='CyberWatch Api Tools.',
    long_description=open('README.md').read().strip(),
    long_description_content_type="text/markdown",
    version='2.0.4',
    author='CyberWatch SAS',
    author_email='support-it+api@cyberwatch.fr',
    license='MIT',
    url='https://github.com/Cyberwatch/cyberwatch_api_toolbox',
    project_urls={
        "Documentation": "https://docs.cyberwatch.fr/api/#introduction",
    },
    py_modules=['cbw-api-toolbox'],
    zip_safe=False,
    packages=['cbw_api_toolbox'],
    package_dir={'cbw_api_toolbox': 'cbw_api_toolbox'},
    install_requires=[
        "requests>=2.20.1",
        "XlsxWriter>=1.2.1",
        "xlrd>=1.2.0"
    ]
)
