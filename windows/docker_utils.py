import os


class docker_utility:
    docker_url = "https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
    # TODO: find correct installlation path
    docker_install_path = ''
    docker_path: str
    is_valid_install: bool

    def __init__(self):
        self.docker_path = ''
        self.is_valid_install = False

    def check_docker_installation(self, PATH=os.getenv('PATH')):
        print('Verifying Docker Installation.')

    def get_docker_version(self):
        print('Docker version.')

    def clean_docker(self):
        print('Cleaning Docker.')
        print('Docker Cleaned.')

    def uninstall_docker(self):
        print('Uninstalling Docker.')

    def find_docker_in_PATH(self, PATH=os.getenv('PATH')) -> bool:
        return self.is_valid_install

    def install_docker(self, PATH=os.getenv('PATH')):
        print('Installing Docker.')