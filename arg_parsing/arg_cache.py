import argparse
from argparse import ArgumentParser



def parse_args():
    parser = argparse.ArgumentParser(description='An install application for an ECS dev system')

    parser.add_argument('-t', '--token',
                        metavar='token',
                        type=str,
                        default="NO TOKEN",
                        help="Your github token")

    parser.add_argument('-c', '--clean',
                        action='store_true',
                        default=False,
                        help="A clean install. Removes current Minikube configuration")
    parser.parse_args()