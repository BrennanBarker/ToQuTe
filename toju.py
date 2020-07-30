from argparse import ArgumentParser
import sys
from jupyter_client import find_connection_file, BlockingKernelClient


def get_kwargs():
    parser = ArgumentParser(prog='toju',
                            description=('Interact with a Jupyter kernel from '
                                        'the command line.'))
    parser.add_argument('code', action='store', nargs='?', default=sys.stdin)
    kwargs = vars(parser.parse_args())

    if hasattr(kwargs['code'], 'read'):  # If stdin or file get contents
        kwargs['code'] = kwargs['code'].read()

    return kwargs


def main(code):
    client = BlockingKernelClient()
    client.load_connection_file(find_connection_file())
    client.execute(code, allow_stdin=False)


if __name__ == '__main__':
    kwargs = get_kwargs()
    main(**kwargs)
