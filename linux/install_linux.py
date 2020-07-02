import argparse
import docker_utils
import helm_utils
import kubectl_utils
import minikube_utils
import subprocess
import time

# Default values of arguments
SIZE_OF_DEPLOYMENT = "M"
REPO_PRIVATE_TOKEN = ""

docker_gpg = "https://download.docker.com/linux/ubuntu/gpg"

def install_tux(args: argparse.ArgumentParser):
    print('Beginning install process for Linux...')
    execute_docker(args)
    execute_minikube(args)
    execute_kubectl(args)
    execute_helm(args)

def execute_docker(args: argparse.ArgumentParser):
    docker_util = docker_utils.docker_utility()

    # TO DO, probably through just folder removal
    # if args.clean:
        # docker_util.clean_docker()

    # Start install
    docker_util.install_docker()

def execute_helm(args: argparse.ArgumentParser):
    helm_util = helm_utils.helm_utility()

    if args.clean or args.helm_clean:
        helm_util.clean_helm()

    # Start install
    helm_util.install_helm()

def execute_kubectl(args: argparse.ArgumentParser):
    kubectl_util = kubectl_utils.kubectl_utility()

    if args.clean:
        kubectl_util.clean_kubectl()

    # Start install
    kubectl_util.install_kubectl()

def execute_minikube(args: argparse.ArgumentParser):
    minikube_util = minikube_utils.minikube_utility()

    if args.clean or args.minikube_clean:
        minikube_util.clean_minikube()

    # Start install
    minikube_util.install_minikube()

def verify_installation():
    print('Verifying installation')
    isValidInstall = False

    #TODO: Validate install. Perhaps provide a diagnosis.

    return isValidInstall

