import os
import ctypes
import argparse
import time
import subprocess
import windows.minikube_utils
import windows.objectscale_utils
import windows.helm_utils
import windows.cert_utils

# Pathing variables.
PATH = os.getenv('PATH')

# Main function
def install_win(args: argparse.ArgumentParser, certs_found: bool):
    print('Beginning install process for Windows.')

    # Check for UAC elevation.
    if not is_admin():
        print('This installer needs to be run as an ' + colors.bold + 'admin.' + colors.reset)
        return

    print(os.getcwd())

    install_certs(args)

    install_minikube(args)

    install_helm(args)

    install_docker(args)

    install_objectscale(args)

    install_successful = verify_installation(args)

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
        print(
            'No Github token provided. Objectscale needs a token to install properly. Use the -t [Github token] flag to provide a token. See readme.md for more info.')
        print('----- END Objectscale -----\n' + colors.reset)
        return
    objs_util = windows.objectscale_utils.objectscale_utility()
    if args.ECS_clean or args.clean:
        objs_util.clean_objectscale()
        objs_util.uninstall_objectscale()
        objs_util.install_objectscale(args.token)
    elif args.ECS_install:
        objs_util.uninstall_objectscale()
        objs_util.install_objectscale(args.token)
    elif not objs_util.check_objectscale_installation():
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
        print('Helm installed, now re-installing..')
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


def install_certs(args: argparse.ArgumentParser):
    cert_manager = windows.cert_utils.cert_utility()
    print(colors.fg.yellow + "-----Certificates (Windows)-----")
    cert_manager.make_certs_folder()
    pem_certs_found, cer_certs_found = cert_manager.count_certs()
    if pem_certs_found == 0 and cer_certs_found == 0 and not (args.pull_certs or args.pull_certs_force):
        print('Certs not detected, helm charts and images may not pull properly.')
        print('On windows, use the --pull-certs flag to automatically fetch the certs,')
        print('or place the certificates by hand into the certs folder.')
    elif pem_certs_found + cer_certs_found < cert_manager.certs_expected and not (args.pull_certs or args.pull_certs_force):
        print('Found ' + str(cer_certs_found+pem_certs_found) + ', expected minimum ' + str(cert_manager.certs_expected)+'.')
        print('Not having the proper certificates may cause connectivity issues within the VM.')
        print('If connectivity problems persist, run this installer with the --pull-certs ')
        print('flag to attempt to automatically pull certs.')
    elif (args.pull_certs and pem_certs_found == 0 and cer_certs_found == 0) or args.pull_certs_force:
        print('Found ' + str(cer_certs_found + pem_certs_found) + ', expected minimum ' + str(cert_manager.certs_expected)+'.')
        print('Pulling certificates')
        cert_manager.pull_certs(args.pull_certs_force)
    else:
        print('Certificates found in folder.')

    if (args.pull_certs_force or cer_certs_found > 0 or (args.pull_certs and pem_certs_found == 0 and cer_certs_found == 0)) and not args.pull_certs_no_convert:
        print('Converting certificates to PEM format.')
        cert_manager.convert_certs()
    elif (args.pull_certs_force or cer_certs_found > 0 or (args.pull_certs and pem_certs_found == 0 and cer_certs_found == 0)) and args.pull_certs_no_convert:
        print('No convert flag specified, skipping conversion.')

    print('Copying certificates to minikube.')
    cert_manager.move_certs_to_minikube()
    print("----- End Certificates (Windows) -----" + colors.reset)


def verify_installation(args: argparse.ArgumentParser) -> bool:
    print(colors.fg.purple + '-----Verifying installation-----')
    isValidInstall = True
    # Give minikube some time to construct containers.
    time.sleep(1)

    if not check_minikube():
        print(colors.bg.red + colors.bold + colors.fg.black + 'Minikube not Found!' + colors.reset + colors.fg.purple)
        isValidInstall = False
    else:
        print('Minikube installed correctly!')
    if not check_helm():
        print(colors.bg.red + colors.bold + colors.fg.black + 'Helm not Found!' + colors.reset + colors.fg.purple)
        isValidInstall = False
    else:
        print('Helm installed correctly!')
    if not check_objectscale():
        print(
            colors.bg.red + colors.bold + colors.fg.black + 'Objectscale not Installed properly!' + colors.reset + colors.fg.purple)
        isValidInstall = False
    else:
        print('Objectscale installed correctly!')
    # TODO: Validate install. Perhaps provide a diagnosis.

    print('----- End Verification -----' + colors.reset)
    return isValidInstall


def check_minikube() -> bool:
    result = subprocess.check_output('minikube version', shell=True)
    result = result.decode(encoding='ascii')
    return result.find('minikube version: ') > -1


def check_helm() -> bool:
    result = subprocess.check_output('helm version', shell=True)
    result = result.decode(encoding='ascii')
    return result.find('version.version{') > -1


def check_objectscale() -> bool:
    return False


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
