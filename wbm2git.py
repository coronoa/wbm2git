import requests
import re
from bs4 import BeautifulSoup
import os
import git
import logging


default_config = dict(
    git_user_name='None',
    git_user_email='None',
    filename='content.html',
    css_selector_content='#content',
    css_selector_time='#date',
)


class Run:
    source_url = None
    git_repo_path = None
    config = None
    _git_repo = None
    _wbm_url = 'https://web.archive.org/cdx/search?url={source_url}&output=json'
    _content_url = 'https://web.archive.org/web/{timestamp}/{source_url}'
    _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    def __init__(self, source_url: str, git_repo_path: str, config: dict = None) -> None:
        self.source_url = source_url
        self.git_repo_path = git_repo_path
        self.config = config or default_config
        self.run()

    def run(self) -> None:
        self.create_git_repo()
        for timestamp in self.get_wbm_timestamps():
            full_html = self.get_wbm_html(timestamp)
            required_content, content_time = self.parse_html(full_html)
            self.commit_content(required_content, content_time)

    def get_wbm_timestamps(self) -> list:
        wbm_json = requests.get(self._wbm_url.format(source_url=self.source_url), headers=self._headers).json()
        del wbm_json[0]
        timestamps = list()
        for version in wbm_json:
            timestamps.append(int(version[1]))
        return timestamps

    def get_wbm_html(self, timestamp) -> str:
        content_url = self._content_url.format(source_url=self.source_url, timestamp=timestamp)
        logging.info('-- wbm2git: request content for timestamp %i' % timestamp)
        html = requests.get(content_url, headers=self._headers).text
        return html

    # noinspection PyMethodMayBeStatic
    def parse_html(self, website_full_html) -> (str, int):
        soup = BeautifulSoup(website_full_html, features='html.parser')
        content_html = soup.select(self.config['css_selector_content'])[0].prettify()
        if not content_html:
            raise ValueError('could not parse html')
        # todo select time somehow general
        time = 0
        content_html = self.rewrite_links(content_html)
        return content_html, time

    # noinspection PyMethodMayBeStatic
    def rewrite_links(self, content_html: str) -> str:
        content_html = re.sub('/web/(\d*)im_/', '', content_html)
        content_html = re.sub('/web/(\d*)/', '', content_html)
        content_html = re.sub('https://web.archive.org/web/(\d*)/', '', content_html)
        return content_html

    def create_git_repo(self) -> None:
        # todo create path if necessary
        # todo first check if git repo already exists
        self._git_repo = git.Repo.init(self.git_repo_path)
        open(os.path.join(self.git_repo_path, self.config['filename']), 'a').close()
        self.check_and_set_git_user()
        self._git_repo.git.add(self.config['filename'])

    def check_and_set_git_user(self) -> None:
        # todo first check if user name is set
        self._git_repo.config_writer().set_value('user', 'name', self.config['git_user_name']).release()
        self._git_repo.config_writer().set_value('user', 'email', self.config['git_user_email']).release()

    def commit_content(self, content: str, time: int) -> None:
        filepath = os.path.join(self.git_repo_path, self.config['filename'])
        with open(filepath, 'w') as file:
            file.write(content)
        self._git_repo.git.add(self.config['filename'])
        self._git_repo.index.commit('update %s' % time)
        logging.info('-- wbm2git: commited')
