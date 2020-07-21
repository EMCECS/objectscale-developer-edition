import os
from os import path
import subprocess
import urllib.request


class minikube_utility:
    minikube_url = "https://github.com/kubernetes/minikube/releases/download/v1.11.0/minikube-windows-amd64.exe"
    minikube_install_path = 'C:\\WINDOWS\\system32'
    minikube_path: str
    is_valid_install: bool

    def __init__(self):
        self.minikube_path = ''
        self.is_valid_install = False

    def check_minikube_installation(self, PATH=os.getenv('PATH')):
        print('Verifying Minikube installation.')

        self.is_valid_install = self.find_minikube_in_PATH(PATH=PATH)

        return self.is_valid_install, self.minikube_path

    def get_minikube_version(self):
        result = subprocess.check_output('Minikube version', shell=True)
        result = result.decode(encoding='ascii')
        return result

    def clean_minikube(self):
        # Let minikube remove itself.
        print('Cleaning Minikube.')
        os.system('minikube stop')
        os.system('minikube delete --all')
        os.system('minikube config set memory 16384')
        os.system('minikube config set cpus 4')
        os.system('minikube config set vm-driver hyperv')
        os.system('minikube config set disk-size 200G')
        if not path.exists(os.getenv('HOMEPATH')+'\\.minikube'):
            os.mkdir(os.getenv('HOMEPATH')+'\\.minikube')
        if not path.exists(os.getenv('HOMEPATH')+'\\.minikube\\files'):
            os.mkdir(os.getenv('HOMEPATH')+'\\.minikube\\files')
        if not path.exists(os.getenv('HOMEPATH')+'\\.minikube\\files\\etc'):
            os.mkdir(os.getenv('HOMEPATH')+'\\.minikube\\files\\etc')
        if not path.exists(os.getenv('HOMEPATH')+'\\.minikube\\files\\etc\\ssl'):
            os.mkdir(os.getenv('HOMEPATH')+'\\.minikube\\files\\etc\\ssl')
        if not path.exists(os.getenv('HOMEPATH')+'\\.minikube\\files\\etc\\ssl\\certs'):
            os.mkdir(os.getenv('HOMEPATH')+'\\.minikube\\files\\etc\\ssl\\certs')
        #os.system('ROBOCOPY certs '+os.getenv('HOMEPATH')+'\\.minikube\\files\\etc\\ssl\\certs *.pem')
        print('Minikube cleaned.')

    def uninstall_minikube(self):
        # Note that this only removes the minikube EXE,
        # This should never be used before running clean_minikube()
        # This should always be called after running check_minikube_installation()
        if self.is_valid_install:
            os.system('del /F /Q "' + self.minikube_path + '\\minikube.exe"')
            print('Minikube deleted.')
        else:
            print('Minikube not found in PATH, skipping removal...')

    def find_minikube_in_PATH(self, PATH=os.getenv('PATH')) -> bool:

        # Split into paths to search for minikube
        paths = PATH.split(';')
        for filePath in paths:
            if not os.path.isdir(filePath):
                paths.remove(filePath)

        # Accumulate list of files until minikube.exe is found.
        files = []
        for filePath in paths:
            files.extend([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
            if 'minikube.exe' in files:
                self.is_valid_install = True
                self.minikube_path = filePath
                break

        return self.is_valid_install

    def install_minikube(self, PATH=os.getenv('PATH')):
        # Change to user downloads folder
        current_path = os.getcwd()
        os.chdir(os.getenv('HOMEPATH') + '\\Downloads')
        if path.exists(os.getenv('HOMEPATH') + '\\Downloads\\minikube.exe'):
            print('Deleting old installer.')
            os.system('del /F /Q minikube.exe')
        print('Starting Download.')
        local_filename, headers = urllib.request.urlretrieve(self.minikube_url, 'minikube.exe')
        print('Installing minikube.')
        os.system('MOVE /Y minikube.exe \"' + self.minikube_install_path + '\\minikube.exe\"')

        old_path = PATH
        try:
            is_valid = self.find_minikube_in_PATH(PATH=PATH)
            if not is_valid:
                print('Adding minikube to PATH..')
                #NOTE: Find a way to persistently set the PATH variable AND get around the limit of 1024 characters
                os.environ['PATH'] = PATH + ';' + self.minikube_install_path
            else:
                print('Minikube installed and ready to use from the command line.')
        except:
            os.environ['PATH'] = old_path

        os.system('minikube config set memory 16384')
        os.system('minikube config set cpus 4')
        os.system('minikube config set vm-driver virtualbox')
        os.chdir(current_path)
