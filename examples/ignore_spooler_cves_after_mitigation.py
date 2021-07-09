"""Script used to ignore related Microsoft CVEs when the spooler service is detected as disabled"""
import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))



CVE_CODES = ['CVE-2021-1675','CVE-2021-34527']

def disabled_spooler_assets():
    '''finds assets with a disabled startup spooler service'''
    params = {
    "service_name": "spooler",
    "service_status": "disabled"
    }

    return CLIENT.assets(params)

def vulnerable_assets():
    '''returns any asset vulnerable to the CVEs'''
    assets = []

    for code in CVE_CODES:
        assets = assets + CLIENT.cve_announcement(code).servers
    return list(uniq(assets))

def uniq(asset_list):
    '''filter the assets list for unicity'''
    last = None
    sorted(asset_list, key=lambda k: k.hostname)
    for asset in sorted(asset_list, key=lambda k: k.hostname):
        if asset.hostname == last.hostname if last else None:
            continue
        yield asset
        last = asset

def ignore():
    '''query Cyberwatch to ignore the CVEs for the appropriate assets'''
    ignored = []

    params = {
        "comment": "The spooler is disabled on this asset",
        "ignored": "true"
    }

    disabled  = disabled_spooler_assets()

    for asset in vulnerable_assets() :
        if any(d.id == asset.id for d in disabled):
            for code in CVE_CODES :
                CLIENT.update_server_cve(str(asset.id), code, params)
                ignored.append([code,asset])

    return ignored

result = ignore()
print('\n=========== Total of {} CVEs have been ingored on disabled spooler assets ==========='.format(len(result)))

for item in result:
    print('{} --- {} --- {}'.format(item[1].id, item[1].hostname, item[0]))
