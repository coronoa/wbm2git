import requests
import re


class SnapWaybackVersions:
    source_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Steckbrief.html'
    wayback_url = 'https://web.archive.org/cdx/search?url={source_url}&output=json'
    content_url = 'https://web.archive.org/web/{timestamp}/{source_url}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    def __init__(self):
        versions = self.get_versions_data()
        for version in versions:
            timestamp = int(version[1])
            self.save_content_to_storage(timestamp)

    def get_versions_data(self):
        wayback_json = requests.get(self.wayback_url.format(source_url=self.source_url), headers=self.headers).json()
        del wayback_json[0]
        return wayback_json

    def save_content_to_storage(self, timestamp: int):
        html = self.request_version_html(timestamp)
        content_html = self.parse_content_from_html(html)
        content_html = self.rewrite_links(content_html)
        filename = 'version_%i.html' % timestamp
        with open(filename, 'w') as file:
            file.write(content_html)
            print('-- saved content to %s' % filename)

    def request_version_html(self, timestamp):
        content_url = self.content_url.format(source_url=self.source_url, timestamp=timestamp)
        print('-- request content for timestamp %i' % timestamp)
        html = requests.get(content_url, headers=self.headers).text
        return html

    def parse_content_from_html(self, html):
        content = re.search('<div id="content">(.*)<!-- #content -->', html, re.DOTALL)
        if not content:
            raise ValueError('could not parse html')
        content_html = '<div id="content">%s' % content.group(1)
        return content_html

    def rewrite_links(self, content_html):
        content_html = re.sub('/web/(\d*)im_/', '', content_html)
        content_html = re.sub('https://web.archive.org/web/(\d*)/', '', content_html)
        return content_html


SnapWaybackVersions()




