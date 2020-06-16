import argparse
from argparse import ArgumentParser

parser = argparse.ArgumentParser(description='An install application for an ECS dev system')

parser.add_argument('-t', '--token',
                    metavar='token',
                    type=str,
                    default="",
                    help="Your github token")

parser.add_argument('-c', '--clean',
                    action='store_true',
                    default="",
                    help="A clean install. Removes current Minikube configuration")


def parse_args(args=[]):
    parser.parse_args(args)