import os
import shutil
import git
from environs import Env

env = Env()
env.read_env()


class VersionizeContent:
    source_directory = 'saved_content'
    git_directory = '../rkisteckbrief_versions'
    git_repo = None

    def __init__(self):
        open(os.path.join(self.git_directory, 'content.html'), 'a').close()
        self.git_repo = git.Repo.init(self.git_directory)
        self.git_repo.config_writer().set_value('user', 'name', env('GIT_USER_NAME')).release()
        self.git_repo.config_writer().set_value('user', 'email', env('GIT_USER_EMAIL')).release()
        self.git_repo.git.add('content.html')

        version_files = os.listdir(self.source_directory)
        version_files.sort()

        for filename in version_files:
            if filename.endswith('.html'):
                self.commit_with_git(filename)

    def commit_with_git(self, filename):
        path = os.path.join(self.source_directory, filename)
        shutil.copy(path, os.path.join(self.git_directory, 'content.html'))
        self.git_repo.git.add('content.html')
        print(self.git_repo.index.commit('update %s' % filename))


VersionizeContent()
