import argparse
from pathlib2 import Path
from .commands import COMMANDS


def parse_args(description, args):
    p = argparse.ArgumentParser(description=description)

    p.add_argument(
        '--datadir',
        dest='DATADIR',
        type=Path,
        default=Path.home() / '.zcash',
        help='Node datadir.',
    )

    p.add_argument(
        '--debug',
        dest='DEBUG',
        action='store_true',
        default=False,
        help='Debug output.',
    )

    subp = p.add_subparsers()
    for (name, f) in COMMANDS.iteritems():
        cmdp = subp.add_parser(name.replace('_', '-'), help=f.__doc__)
        cmdp.set_defaults(func=f)

    return p.parse_args(args)
