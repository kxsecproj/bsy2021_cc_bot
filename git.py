
import os


class Git:
    """
            # gist.github communication class.
    """
    def __init__(self, token, url, repo):
        """
        :param repo: directory of gist.github repository.
        :param token: token of github account.
        :param url: url to gist.github repository.
        """
        self.token = token
        self.url = url
        self.repo = repo

    def clone(self):
        """
        Clone gist.github repository.
        """
        os.system("git clone "+self.url+" &> /dev/null")

    def push(self, file):
        """
        Push file to the repository.
        :param file: file to be pushed.
        """
        os.system("cd " + self.repo + "; git add " + file + " &> /dev/null; git commit -m '...' &> /dev/null")
        os.system("cd " + self.repo + "; git push https://" + self.token
                  + "@gist.github.com/" + self.repo + ".git &> /dev/null")

    def push_all(self):
        """
        Push all changes to the repository.
        """
        os.system("cd " + self.repo + " ; git commit -m '...' --quiet; git push https://" + self.token +
                  "@gist.github.com/" + self.repo + ".git &> /dev/null")

    def pull(self):
        """
        Actualise repository and download changes.
        """
        os.system("cd " + self.repo + "; git pull &> /dev/null")
