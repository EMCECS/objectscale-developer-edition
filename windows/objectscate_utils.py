import os


class objectscale_utility:
    # TODO: find correct URL, if applicable.
    objectscale_url = ""
    # TODO: find correct installlation path
    objectscale_install_path = ''
    objectscale_path: str
    is_valid_install: bool

    def __init__(self):
        self.objectscale_path = ''
        self.is_valid_install = False

    def check_objectscale_installation(self, PATH=os.getenv('PATH')):
        print('Verifying objectscale Installation.')

    def get_objectscale_version(self):
        print('objectscale version.')

    def clean_objectscale(self):
        print('Cleaning objectscale.')
        print('objectscale Cleaned.')

    def uninstall_objectscale(self):
        print('Uninstalling objectscale.')

    def find_objectscale_in_PATH(self, PATH=os.getenv('PATH')) -> bool:
        return self.is_valid_install

    def install_objectscale(self, PATH=os.getenv('PATH')):
        print('Installing objectscale.')
