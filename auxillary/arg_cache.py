import os
import argparse


class parse_cache:
    parser = ''
    args = ''

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='An install application for an ECS dev environment')
        self.parser.add_argument('-t', '--token',
                                 dest='token',
                                 type=str,
                                 default="NO TOKEN",
                                 help="Your github token")

        self.parser.add_argument('-c', '--clean',
                                 action='store_true',
                                 default=False,
                                 dest='clean',
                                 help="A clean install of all components. Removes all configurations of all "
                                      "namespaces on local machine")

        self.parser.add_argument('-mc', '--minikubeClean',
                                 action='store_true',
                                 default=False,
                                 dest='minikube_clean',
                                 help='Destroy current Minikube configuration and start fresh.')

        self.parser.add_argument('-mi', '--minikubeInstall',
                                 action='store_true',
                                 default=False,
                                 dest='minikube_install',
                                 help='Reinstall the Minikube system, even if currently installed.')

        self.parser.add_argument('-hc', '--helmClean',
                                 action='store_true',
                                 default=False,
                                 dest='helm_clean',
                                 help='Destroy current Helm configuration and start fresh.')

        self.parser.add_argument('-hi', '--helmInstall',
                                 action='store_true',
                                 default=False,
                                 dest='helm_install',
                                 help='Reinstall the Helm system, even if currently installed.')

        self.parser.add_argument('-oi', '--ObjectscaleInstall',
                                 action='store_true',
                                 default=False,
                                 dest='ECS_install',
                                 help='Reinstall ECS pods, and helm charts.')

        self.parser.add_argument('-oc', '--ObjectscaleClean',
                                 action='store_true',
                                 default=False,
                                 dest='ECS_clean',
                                 help='Destroy ECS cluster and remove all local data.')

        self.parser.add_argument('-pc', '--pull-certs',
                                 action='store_true',
                                 default=False,
                                 dest='pull_certs',
                                 help='(Windows only) attempt to automatically pull SSL certificate files from the registry.')

        self.parser.add_argument('-pcf', '--pull-certs-force',
                                 action='store_true',
                                 default=False,
                                 dest='pull_certs_force',
                                 help='(Windows only) pull certificates, even if they already exist in the certs folder.')

        self.parser.add_argument('-pcnc', '--no-convert',
                                 action='store_true',
                                 default=False,
                                 dest='pull_certs_no_convert',
                                 help='(Windows only) do not convert certificates from CER to PEM. This will prevent them from being copied to Minikube.')

        self.parser.add_argument('-pcr', '--certificate-regex',
                                 type=str,
                                 dest='cert_regex',
                                 default='Subject.*CN=.*(emc|EMC)',
                                 help='(Windows only) do not convert certificates from CER to PEM. This will prevent them from being copied to Minikube.')

        self.parser.add_argument('--versions',
                                 action='store_true',
                                 default=False,
                                 dest='versions_query',
                                 help='Query the available versions of objectscale to install.')

        self.parser.add_argument('-v', '--version',
                                 type=str,
                                 dest='version',
                                 default='v0.33.0',
                                 help='The version of objectscale to be installed.')


    @staticmethod
    def getFolderDirectory() -> str:
        path = os.path.dirname(os.path.realpath(__file__))[:-12]
        return path
