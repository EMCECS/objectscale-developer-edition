import os
import os.path
import ctypes
import argparse
import arg_parsing.arg_cache
import windows.minikube_utils
import windows.objectscale_utils
import windows.helm_utils

# URLs for grabbing programs
deos_url = "raw.githubusercontent.com/emecs/charts/master/docs"
docker_url = "https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe"

# Pathing variables.
PATH = os.getenv('PATH')

install_successful = False


# Main function
def install_win(args: argparse.ArgumentParser):
    print('Beginning install process for Windows.')

    # Check for UAC elevation.
    if not is_admin():
        print('This installer needs to be run as an ' + colors.bold + 'admin.' + colors.reset)
        return

    install_minikube(args)

    install_helm(args)

    install_docker(args)

    install_objectscale(args)

    verify_installation(args)

    # TODO: implement validity check for installation
    if install_successful:
        print(' Installation complete! ')
        print('use \'kubectl get pods\' to verify installation.')
    else:
        print('Installation failed. See output for details.')


def is_admin() -> bool:
    run_as_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return run_as_admin


def install_objectscale(args: argparse.ArgumentParser):
    print(colors.fg.lightred + '-----Objectscale-----')
    # TODO: use helm to install objectscale
    if args.token == 'NO TOKEN':
        print('No Github token provided. Objectscale needs a token to install properly. Use the -t [Github token] flag to provide a token. See readme.md for more info.')
        print('----- END Objectscale -----\n' + colors.reset)
        return
    objs_util = windows.objectscale_utils.objectscale_utility()
    if not objs_util.check_objectscale_installation():
        print('Installing Objectscale ECS cluster')
        objs_util.install_objectscale(args.token)
    print('----- END Objectscale -----\n' + colors.reset)


def install_docker(args: argparse.ArgumentParser):
    print(colors.fg.blue + '-----Docker-----')
    # TODO: Verify docker installation
    print('----- END Docker -----\n' + colors.reset)


def install_helm(args: argparse.ArgumentParser):
    print(colors.fg.green + '-----Helm------')
    helm_util = windows.helm_utils.helm_utility()
    helm_installed, helm_path = helm_util.check_helm_installation()
    if helm_installed and not (args.clean or args.helm_clean or args.helm_install):
        print('Helm found!')
        print('Found at ' + helm_util.helm_path)
        helm_util.get_helm_version()
    elif not helm_installed:
        helm_util.install_helm()

    if args.helm_install:
        print('minikube installed, now re-installing..')
        helm_util.uninstall_helm()
        helm_util.install_helm()

    if args.clean or args.helm_clean:
        print('Removing local data')
        helm_util.clean_helm()

    print('----- END Helm -----\n' + colors.reset)


def install_minikube(args: argparse.ArgumentParser):
    print(colors.fg.lightcyan + '-----Minikube-----')
    minikube_util = windows.minikube_utils.minikube_utility()
    minikube_installed, minikube_path = minikube_util.check_minikube_installation()

    if minikube_installed and not (args.clean or args.minikube_clean or args.minikube_install):
        print('Minikube installation found! installed at  ')
        print(minikube_path)
        minikube_util.get_minikube_version()

    elif not minikube_installed:
        print('Minikube not found, installing minikube')
        minikube_util.install_minikube()

    if args.minikube_install:
        print('minikube installed, now re-installing..')
        minikube_util.uninstall_minikube()
        minikube_util.install_minikube()

    if args.clean or args.minikube_clean:
        print('Removing local data')
        minikube_util.clean_minikube()
    print('----- END Minikube -----\n' + colors.reset)


def verify_installation(args: argparse.ArgumentParser) -> bool:
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
