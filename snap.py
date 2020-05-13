import requests


class SnapWaybackVersions:
    source_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Steckbrief.html'
    wayback_url = 'https://web.archive.org/cdx/search?url={source_url}&output=json'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    def __init__(self):
        versions = self.get_versions_data()
        for version in versions:
            print(version[1])

    def get_versions_data(self):
        wayback_json = requests.get(self.wayback_url.format(source_url=self.source_url), headers=self.headers).json()
        del wayback_json[0]
        return wayback_json


SnapWaybackVersions()




