import os
from os import path
import subprocess

class verification_util():
    allverified = False

    powershell_verified = False

    def __init__(self):
        self.allverified = False

    def run_command_get_all_output(self, command: str, Shell=True,stderr=subprocess.STDOUT) -> str:
        output = ''
        try:
            output = subprocess.check_output(command, Shell=Shell,stderr=stderr)
        except subprocess.CalledProcessError as e:
            output = e.output.decode(encoding='ascii')
        except Exception as e:
            return e.output.decode(encoding='ascii')

        return output

    # verifies that powershell is available, returning an empty string if it is not available
    def verify_powershell(self) -> str:
        #Check the default install location, then if not found, check the PATH
        if path.exists('C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'):
            self.powershell_verified = True
            return 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
        else:
            return self.find_in_path('powershell.exe')

    # Verifies the version, config, and files pertaining to minikube
    # Returns a blank string if not configured properly
    def verify_minikube(self) -> str:
        # A set of commands and paths that re used to verify that the Minikube installation is good.
        # Path 1: The path to the minikube installation folder. It is used to check config files, and the presence of PEM files
        # Command 2: A command to check the version of Minikube. This is used moreso to verify that minikube is in the PATH than to get the version.
        # Command 3: Checks the current configuration of Minikube. Used to make sure that the kube is properly configures for Objectscale.
        minikube_cert_path = path.join(os.getenv('HOMEPATH'), '.minikube', 'config')
        kube_version_command = 'minikube version'
        kube_config_list = 'minikube config view'

        version_output = subprocess.check_output(kube_version_command, Shell=True)
        config_output = subprocess.check_output(kube_config_list, Shell=True)
        if version_output.find('minikube version: ') > -1:
            version = version_output[18:version_output.find('\r')]
        else:
            version = ''

        cfg_info = ''
        if config_output.find('- cpus: 4') > -1:
            cfg_info += 'c4'
        if config_output.find('- memory: 16384') > -1:
            cfg_info += 'm16384'
        if config_output.find('- vm-driver: virtualbox') > -1:
            cfg_info += 'vmvb'

        return version+cfg_info


    # Verifies the proper helm charts are installed and charted properly.
    def verify_helm(self) -> str:
        helm_version_command = 'helm version'

    # Verifies that objectscale is running and
    # has a proper endpoint. If objectscale is in a state of error,
    # the method returns a string describing an error, otherwise
    # returns a blank string
    def verify_Objectscale(self) -> str:
        # Set of commands that are used to get important information.
        # Command 1: returns the status of the minikube cluster
        # Command 2: returns the pods which are active
        # TODO: insert command to change the namespace to Objectscale
        # Command 3:
        kube_status_command = 'minikube status'
        workspace_status_command = 'kubectl get namespaces'
        pod_status_command = 'kubectl get pods'

        kube_status_result = ''
        try:
            kube_status_result = subprocess.check_output(kube_status_command,Shell=True,stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            kube_status_result = e.output.decode(encoding='ascii')



    # Internal method to look for items in the path.
    # if the item is found, it returns the path, otherwise
    # it returns an empty string.
    def find_in_path(self, item, PATH=os.getenv('PATH')) -> str:
        # Split into paths to search for minikube
        paths = PATH.split(';')
        for filePath in paths:
            if not os.path.isdir(filePath):
                paths.remove(filePath)

        # Accumulate list of files until item is found.
        files = []
        for filePath in paths:
            files.extend([f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))])
            if item in files:
                return filePath
        return ''