import os

# Currently a vestigial class.
# Docker for windows is installed via GUI only.
class docker_utility:
    docker_path: str
    is_valid_install: bool

    def __init__(self):
        self.docker_path = ''
        self.is_valid_install = False

    # TODO: implement.
    def check_docker_installation(self, PATH=os.getenv('PATH')):
        print('Verifying Docker Installation.')

    # TODO: implement.
    def get_docker_version(self):
        print('Docker version.')

    # TODO: needed?
    def clean_docker(self):
        print('Cleaning Docker.')
        print('Docker Cleaned.')

