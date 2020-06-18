import os
from os import path
import subprocess

class minikube_utility:
    minikube_url = "https://github.com/kubernetes/minikube/releases/latest/download/minikube-installer.exe"
    minikube_path : str
    is_valid_install : bool

    def __init__(self):
        self.minikube_path = ''
        self.is_valid_install = False

    def check_minikube_installation(self,PATH = 'C:\Windows'):
        print('Verifying Minikube Installation')

        #split into paths to search for minikube
        paths = PATH.split(';')
        for filePath in paths:
            if not os.path.isdir(filePath):
                paths.remove(filePath)

        #acumulate list of files until minikube.exe is found.
        files = []
        for filePath in paths:
            files.extend([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
            if 'minikube.exe' in files:
                self.is_valid_install = True
                self.minikube_path = filePath
                break

        return self.is_valid_install, self.minikube_path

    def get_minikube_version(self):
        result = subprocess.check_output('minikube version', shell=True)
        result = result.decode(encoding='ascii')
        print(result)
        return result


    def clean_minikube(self):
        # Let minikube remove itself.
        os.system('minikube stop')
        os.system('minikube delete --all')
        os.system('minikube delete --purge')
        print('minikube cleaned!')

    def uninstall_minikube(self):
        # Note that this only removes the minikube EXE,
        # This should never be used before running clean_minikube()
        # This should always be called after running check_minikube_installation()
        current_path = os.getcwd()
        if self.is_valid_install:
            if path.exists(self.minikube_path+'\\uninstall.exe'):
                os.system('\"'+self.minikube_path+'\\uninstall.exe\"')
                # TODO: wait until process finishes.
            else:
                os.system('del /F /Q '+self.minikube_path+'\\minikube.exe')

            print('minikube deleted!')
        else:
            print('minikube not found in PATH, skipping removal...')

#def install_minikube():`