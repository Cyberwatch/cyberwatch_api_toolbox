"""Download latest scanning scripts for Cyberwatch Importer"""

import argparse
import os
import shutil
from configparser import ConfigParser
import requests
from cbw_api_toolbox.cbw_api import CBWApi

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '../..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client


def clean_directory():
    """Delete old directory if it exists"""
    print("INFO: Cleaning old files...")
    if os.path.exists(os.path.dirname(__file__) + '/Scripts'):
        try:
            shutil.rmtree(os.path.dirname(__file__) + '/Scripts')
        except OSError as error:
            print("Error: %s - %s." % (error.filename, error.strerror))


def make_directory(scripts):
    """Make a directory for each category"""
    if not os.path.exists(os.path.dirname(__file__) + '/Uploads'):
        os.makedirs(os.path.dirname(__file__) + '/Uploads')
    for script_object in scripts:
        path = script_object.type.split('::')
        path = os.path.join(os.path.dirname(__file__) +
                            '/' + "/".join(path[:-1]))
        if not os.path.exists(path):
            os.makedirs(path)


def download_scripts(parsed_args, scripts, client):
    """Get each script and put it in the correct category"""
    print("INFO: Fetching available scanning scripts...")
    for script_object in scripts:
        script = client.fetch_importer_script(str(script_object.id))
        file_name = script.type.split('::')
        if "Linux" in file_name:
            file_name[-1] += '.sh'
        elif "Windows" in file_name:
            file_name[-1] += '.ps1'
        path = os.path.join(os.path.dirname(__file__) +
                            '/' + "/".join(file_name))
        with open(path, 'w') as filehandle:
            filehandle.write(script.contents)
        if script.attachment and parsed_args.no_attachment:
            download_attachment(file_name, script.attachment)
    print("INFO: Script saved at {}".format(
        os.path.dirname(__file__) + '/Scripts'))


def download_attachment(path, url):
    """Download attachment if the script has one"""
    attachment = requests.get(url, allow_redirects=True, verify=False)
    location = os.path.join(os.path.dirname(
        __file__) + '/' + "/".join(path[:-1]))
    name = url.split("/")[-1]
    with open(location + '/' + name, 'wb') as file:
        file.write(attachment.content)


def create_windows_launch_all():
    """Creates a "windows launch all" powershell script"""
    launch_all_powershell = r"""$hostname = [System.Net.Dns]::GetHostName()
    If ( !( Test-Path -Path .\upload )) { New-Item -ItemType Directory -Force -Path .\upload | Out-Null }

    Get-ChildItem -Path $PSScriptRoot -Filter "*.ps1" | ForEach-Object {
    If ($_.FullName -NotLike ("*" + $MyInvocation.MyCommand.Name + "*")) {
        Write-Host ("Current script: " + $_.FullName)
        & $_.FullName > $(".\upload\" + $hostname + "_" + $_.BaseName + ".txt")
        }
    }"""

    path = os.path.join(os.path.dirname(__file__) + "/Scripts/Windows/")
    with open(path + "cbw_launch_all.ps1", 'w') as filehandle:
        filehandle.write(launch_all_powershell)


def launch_script(parsed_args):
    '''Launch script'''
    client = connect_api()
    scripts = client.fetch_importer_scripts()
    clean_directory()
    make_directory(scripts)
    download_scripts(parsed_args, scripts, client)
    create_windows_launch_all()


def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description="Script using Cyberwatch API to get the latest scanning scripts for Cyberwatch Importer")

    parser.add_argument(
        '--no_attachment',
        help='Skip download of scripts attachments (ex: ".cab" file)', default=True,
        action='store_false')

    args = parser.parse_args(args)
    launch_script(args)


if __name__ == '__main__':
    main()
