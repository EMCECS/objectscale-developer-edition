import os
from os import path
import subprocess
import zipfile
import sys
import urllib.request

class kind_utility:
    kind_url = 'https://storage.googleapis.com/kubernetes-release/release/v1.19.0/bin/windows/amd64/kubectl.exe'
    kind_install_path = 'C:\\Windows'
    is_valid_install = False
    helm_path = ''

    def __init__(self):
        self.is_valid_install = False


    def install_kind(self):
        # Change to user downloads folder
        current_path = os.getcwd()
        os.chdir(os.getenv('HOMEPATH') + '\\Downloads')
        if not path.exists(os.getenv('HOMEPATH') + '\\Downloads\\kind.exe'):
            print('Starting Download of Helm.')
            local_filename, headers = urllib.request.urlretrieve(self.kind_url, os.getenv('HOMEPATH') + '\\Downloads\\kind.exe')

        install_path_exists = path.exists(self.kind_install_path)
        if not install_path_exists:
            os.mkdir(self.helm_install_path)

        os.system('ROBOCOPY \"' + os.getenv('HOMEPATH') + '\\Downloads\\kind.exe\" ' + self.kind_install_path + ' /NDL /NFL')


    def check_kind_installation(self, PATH=os.getenv('PATH')):
        print('Verifying kind Installation.')

        self.is_valid_install = self.find_kind_in_PATH(PATH=PATH)

        return self.is_valid_install, self.helm_path


    def find_kind_in_PATH(self, PATH=os.getenv('PATH')) -> bool:

        # Split into paths to search for helm
        paths = PATH.split(';')
        for filePath in paths:
            if not os.path.isdir(filePath):
                paths.remove(filePath)

        # Accumulate list of files until helm.exe is found.
        files = []
        for filePath in paths:
            files.extend([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
            if 'kind.exe' in files:
                self.is_valid_install = True
                self.helm_path = filePath
                break

        return self.is_valid_install

    def clean_kind(self):
        print('Cleaning kind.')
        #TODO: implement with story
