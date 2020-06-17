import os
import os.path
import ctypes

#URLs for grabbing programs
deos_url = "raw.githubusercontent.com/emecs/charts/master/docs"
helm_url = "https://get.helm.sh/helm-v2.16.9-windows-amd64.zip"
docker_url = "https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
minikube_url = "https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe"

#Pathing variables.
PATH = os.getenv('PATH')

#Main function
def install_win():
    print('Beginning install process for Windows.')

    #Check for UAC elevation.
    if not is_admin():
        print('This installer needs to be run as an '+colors.bold+'admin.'+colors.reset)
        return

    print(colors.fg.lightcyan+'Checking for Minikube')
    minikube_installed, minikube_path = check_minikube_installation()
    if minikube_installed:
        print('Minikube installation found! installed at  ')
        print(minikube_path)
    else:
        print('Minikube not found.')
    print(colors.reset)

def is_admin():
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def check_minikube_installation():
    print('Verifying Minikube Installation')

    #split into paths to search for minikube
    is_valid_install = False
    paths = PATH.split(';')
    for filePath in paths:
        if not os.path.isdir(filePath):
            paths.remove(filePath)

    #acumulate list of files until minikube.exe is found.
    files = []
    minikube_path = ''
    for filePath in paths:
        files.extend([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
        if 'minikube.exe' in files:
            is_valid_install = True
            minikube_path = filePath
            break

    return is_valid_install, minikube_path


def verify_installation():
    print('Verifying installation')
    isValidInstall = False

    # TODO: Validate install. Perhaps provide a diagnosis.

    return isValidInstall

class colors:

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'