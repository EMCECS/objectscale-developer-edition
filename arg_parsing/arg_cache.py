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

        self.args = self.parser.parse_args()
