import os
from os import path
import subprocess
import zipfile
import sys
import urllib.request

class helm_utility:
    helm_url = "https://get.helm.sh/helm-v2.16.9-windows-amd64.zip"
    #TODO: Replace the string below with the proper installation location.
    helm_install_path = os.getenv('HOMEPATH') +'\\HELM'
    is_valid_install: bool
    helm_path: str

    def __init__(self):
        self.helm_path = ''
        self.is_valid_install = False

    def check_helm_installation(self, PATH=os.getenv('PATH')):
        print('Verifying helm Installation.')

        self.is_valid_install = self.find_helm_in_PATH(PATH=PATH)

        return self.is_valid_install, self.helm_path

    def find_helm_in_PATH(self, PATH=os.getenv('PATH')) -> bool:

        # Split into paths to search for helm
        paths = PATH.split(';')
        for filePath in paths:
            if not os.path.isdir(filePath):
                paths.remove(filePath)

        # Accumulate list of files until helm.exe is found.
        files = []
        for filePath in paths:
            files.extend([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
            if 'helm.exe' in files:
                self.is_valid_install = True
                self.helm_path = filePath
                break

        return self.is_valid_install

    def get_helm_version(self):
        os.system('Helm version.')
        return

    def clean_helm(self):
        # Let helm remove itself.
        print('Cleaning Helm installation.')
        os.system('helm ls --all --short | \"lib\\xargswin.exe\" -I{} \"helm delete {} --purge\"')
        print('Helm cleaned.')

    def uninstall_helm(self):
        #TODO: uninstalls helm from the system. Should use the path as stored in self.helm_install_path
        if self.is_valid_install:
            os.system('del /F /Q \"' + self.helm_path + '\\helm.exe\"')
            print('Helm deleted.')
        else:
            print('Helm not found in PATH, skipping removal...')
        return

    def install_helm(self, PATH=os.getenv('PATH')):
        #TODO: installs helm on the system. If the helm ececutable is already in the self.helm_install_path, do nothing.

        # Change to user downloads folder
        current_path = os.getcwd()
        os.chdir(os.getenv('HOMEPATH') + '\\Downloads')
        if not path.exists(os.getenv('HOMEPATH') + '\\Downloads\\helm-v2.16.9-windows-amd64.zip'):
            print('Starting Download.')
            local_filename, headers = urllib.request.urlretrieve(self.helm_url, 'helm-v2.16.9-windows-amd64.zip')

        if not path.exists(self.helm_install_path):
            os.mkdir(self.helm_install_path)
        os.system('MOVE /Y helm-v2.16.9-windows-amd64.zip \"' + self.helm_install_path + '\\helm-v2.16.9-windows-amd64.zip\"')
        os.chdir(self.helm_install_path)

        try:
            zip = zipfile.ZipFile('helm-v2.16.9-windows-amd64.zip')
            zip.extractall(self.helm_install_path)
        except:
            print('Problem unzipping helm.')

        old_path = PATH
        try:
            is_valid = self.find_helm_in_PATH(PATH=PATH)
            if not is_valid:
                print('Adding Helm to PATH.')
                #NOTE: Find a way to persistently set the PATH variable AND get around the limit of 1024 characters
                os.environ['PATH'] = PATH + ';C:\\' + self.helm_install_path
                #print(os.getenv('PATH'))
            else:
                print('Helm installed and ready to use from the command line.')
        except:
            print('Issue adding Helm to Path... reverting.')
            print(sys.exc_info())
            os.environ['PATH'] = old_path
            return
        os.chdir(current_path)

        return
