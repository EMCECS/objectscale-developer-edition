import os
import subprocess
import importlib

class objectscale_utility:
    # TODO: find correct URL, if applicable.
    default_helm_chart_url = "https://^@raw.githubusercontent.com/emcecs/charts/$/docs"
    default_git_url = 'EMCECS/charts'
    # TODO: find correct installlation path
    objectscale_install_path = ''
    objectscale_path: str
    is_valid_install: bool

    list_repo_command = ['helm',
                         'repo',
                         'list']

    helm_repo_update_command = 'helm repo update'

    install_objectscale_command = ['helm',
                                   'install',
                                   'objs-mgr',
                                   'ecs/objectscale-manager',
                                   '--set',
                                   'global.registry=asdrepo.isus.emc.com:8099']

    intall_micro_node_command = ['helm',
                                 'install',
                                 'ecs/ecs-cluster',
                                 '--set',
                                 'global.registry=asdrepo.isus.emc.com:8099',
                                 '--generate-name',
                                 '--set',
                                 'storageServer.persistence.size=50Gi',
                                 '--set',
                                 'performanceProfile=Micro',
                                 '--set',
                                 'provision.enabled=True',
                                 '--set',
                                 'storageServer.persistence.protected=True',
                                 '--set',
                                 'enableAdvancedStatistics=False',
                                 '--set',
                                 'managementGateway.service.type=NodePort',
                                 '--set',
                                 's3.service.type=NodePort']

    list_all_charts = ['Helm',
                       'list']

    def __init__(self):
        self.objectscale_path = ''
        self.is_valid_install = False


    def check_objectscale_installation(self, PATH=os.getenv('PATH')) -> bool:
        print('Verifying Objectscale Installation.')
        self.start_minikube_if_stoppped()
        result = self.run_command_get_all_output(self.list_repo_command, shell=True).lower()
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
        print('Uninstalling Objectscale.')
        self.start_minikube_if_stoppped()
        result = self.run_command_get_all_output(self.list_repo_command).lower()
        print(result)
        result = self.run_command_get_all_output(self.list_all_charts).lower()
        print(result)
        results = result.split('\n')
        for s in results:
            if not s.find('ecs-cluster') == -1:
                os.system('helm uninstall ' + s[0:22])
            if not s.find('objs-mgr') == -1:
                os.system('helm uninstall ' + s[0:8])
        print('Objectscale Uninstalled.')

    def install_objectscale(self, token: str, version: str):
        print('Installing Objectscale.')
        self.start_minikube_if_stoppped()
        result = self.run_command_get_all_output('Helm repo list', shell=True)
        print('Installing ecs repo')
        print(self.default_helm_chart_url.replace('^', token).replace('$', version))
        os.system('helm repo add ecs ' + self.default_helm_chart_url.replace('^', token).replace('$', version))
        os.system(self.helm_repo_update_command)
        if result.find('objectscale-helm') == -1:
            print('Installing Objectscale helm dev repo')
            os.system(' '.join(self.install_objectscale_command))
            os.system(' '.join(self.intall_micro_node_command))

        print('Objectscale installed.')

    def start_minikube_if_stoppped(self):
        try:
            result = subprocess.check_output('Minikube status', shell=True)
        except:
            print('Starting Minikube')
            os.system('minikube stop')
            os.system('minikube start --vm-driver=hyperv')
        return

    def run_command_get_all_output(self, command, shell=True, stderr=subprocess.STDOUT) -> str:
        output = ''
        try:
            output = subprocess.check_output(command, shell=False, stderr=stderr)
        except subprocess.CalledProcessError as e:
            print(e.output.decode(encoding='ascii'))
            return e.output.decode(encoding='ascii')
        except Exception as e:
            print(e.output.decode(encoding='ascii'))
            return e.output.decode(encoding='ascii')
        return output.decode(encoding='ascii')
