import os
from os import path
import subprocess
import urllib.request

class helm_utility:
    helm_url = "https://get.helm.sh/helm-v2.16.9-windows-amd64.zip"
    #TODO: Replace the string below with the proper installation location.
    helm_install_path = 'C:\\'
    is_valid_install: bool
    helm_path: str

    def __init__(self):
        self.helm_path = ''
        self.is_valid_install = False

    def check_helm_installation(self, PATH=os.getenv('PATH')):
        print('Verifying helm Installation')

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
        #TODO: prints the string of the helm version, and returns the same string as printed.
        return

    def clean_helm(self):
        # Let minikube remove itself.
        print('Cleaning helm installation')
        os.system('helm ls --all --short | \"lib\\xargswin.exe\" -I{} \"helm delete {} --purge\"')
        print('Helm cleaned!')

    def uninstall_helm(self):
        #TODO: uninstalls helm from the system. Should use the path as stored in self.helm_install_path
        return

    def install_helm(self, PATH=os.getenv('PATH')):
        #TODO: installs helm on the system. If the helm ececutable is already in the self.helm_install_path, do nothing.
        return
