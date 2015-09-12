#!/usr/bin/env python3

import argparse

from sky.view import view


def get_args_parser():
    p = argparse.ArgumentParser(description='sky is the limit.')
    subparsers = p.add_subparsers(dest="command")
    view_parser = subparsers.add_parser('view')
    view_parser.add_argument('-port', '-p', type=int, default=7900)
    view_parser.add_argument('-host', default="localhost")
    return p


def main():
    """ This is the function that is run from commandline with `gittyleaks` """
    args = get_args_parser().parse_args()
    if args.command == 'view':
        view.main(args.host, args.port)
