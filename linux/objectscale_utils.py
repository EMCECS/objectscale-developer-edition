import os
import subprocess


class objectscale_utility:
    # TODO: find correct URL, if applicable.
    helm_chart_url = "https://^@raw.githubusercontent.com/emcecs/charts/$/docs"
    # TODO: find correct installlation path
    objectscale_install_path = ''
    objectscale_path: str
    is_valid_install: bool
    object_manager_install_command = \
        ['helm',
         'install',
         'objs-mgr',
         'ecs/objectscale-manager',
         '--set', 'global.registry=objectscale']
    ecs_cluster_install_command = \
        ['helm',
         'install',
         'ecs/ecs-cluster',
         '--set', 'global.registry=objectscale',
         '--generate-name',
         '--set', 'storageServer.persistence.size=200Gi',
         '--set', 'performanceProfile=Micro',
         '--set', 'provision.enabled=True',
         '--set', 'storageServer.persistence.protected=True',
         '--set', 'enableAdvancedStatistics=False',
         '--set', 'managementGateway.service.type=NodePort',
         '--set', 's3.service.type=NodePort']

    def __init__(self):
        self.objectscale_path = ''
        self.is_valid_install = False

    def check_objectscale_installation(self, PATH=os.getenv('PATH')) -> bool:
        print('Verifying Objectscale Installation.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('Helm init', shell=True)
        result = subprocess.check_output('Helm repo list', shell=True)
        result = result.decode(encoding='ascii').lower()
        if result.find('ecs-cluster') == -1:
            print('ECS-cluster not installed')
            return False
        if result.find('objectscale-manager') == -1:
            print('Objectscale not installed')
            return False
        print('All Objectscale components running, Install not necessary')
        return True

    def get_objectscale_version(self):
        print('Objectscale version.')
        self.start_minikube_if_stoppped()

    def clean_objectscale(self):
        print('Cleaning objectscale.')
        self.start_minikube_if_stoppped()
        print('Objectscale Cleaned.')

    def uninstall_objectscale(self):
        print('Uninstalling objectscale.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('Helm list | "%CD%/lib_distr/gawk/awk.exe" "{print $1}"', shell=True)
        result = result.decode(encoding='ascii').lower()
        results = result.split('\n')
        for s in results:
            if not s.find('ecs-cluster') == -1:
                os.system('helm uninstall ' + s)
            if not s.find('objs-mgr') == -1:
                os.system('helm uninstall ' + s)

    def install_objectscale(self, token: str, version: str, PATH=os.getenv('PATH')):
        print('Installing Objectscale.')
        self.start_minikube_if_stoppped()
        result = self.run_command_get_all_output('helm repo list', shell=True)
        print('Installing Deos repo')
        ecs_repo = self.helm_chart_url.replace('^', token).replace('$', version)
        print(self.run_command_get_all_output(['helm','repo','add','ecs',ecs_repo]))
        print(self.run_command_get_all_output(['helm','repo','update']))
        if result.find('objectscale-helm-dev') == -1:
            print('Installing Objectscale helm dev repo')
            print(self.run_command_get_all_output(self.object_manager_install_command))
            print(self.run_command_get_all_output(self.ecs_cluster_install_command))
            return

    def start_minikube_if_stoppped(self):
        try:
            result = subprocess.check_output('Minikube status', shell=True)
        except:
            print('Starting Minikube')
            os.system('sudo minikube start --vm-driver=none')

    def run_command_get_all_output(self, command, shell=False, stderr=subprocess.STDOUT) -> str:
        output = ''
        try:
            output = subprocess.check_output(command, shell=shell, stderr=stderr)
        except subprocess.CalledProcessError as e:
            print(e.output.decode(encoding='UTF-8'))
            return e.output.decode(encoding='UTF-8')
        except Exception as e:
            return e.output.decode(encoding='UTF-8')
        return output.decode(encoding='UTF-8')
