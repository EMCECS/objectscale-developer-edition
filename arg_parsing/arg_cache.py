import argparse
from argparse import ArgumentParser

parser = argparse.ArgumentParser(description='An install application for an ECS dev system')

parser.add_argument('-t', '--token',
                    #action="store_token",
                    type=str,
                    default="",
                    help="Your github token")


def parse_args(args=[]):
    parser.parse_args(args)