from argparse import ArgumentParser
import sys
from jupyter_client import find_connection_file, BlockingKernelClient


def get_kwargs():
    arg_parser = ArgumentParser(prog='tooqute',
                                description=('Interact with a Jupyter kernel '
                                             'from the command line.'))
    arg_parser.add_argument('action', action='store',
                            choices=['execute', 'complete', 'inspect'])
    arg_parser.add_argument('code', action='store', nargs='?',
                            default=sys.stdin)
    arg_parser.add_argument('-v', '--verbose', action='store_true')
    kwargs = vars(arg_parser.parse_args())

    if hasattr(kwargs['code'], 'read'):  # If stdin or file get contents
        kwargs['code'] = kwargs['code'].read()

    return kwargs


def client_connection_to_kernel():
    client = BlockingKernelClient()
    client.load_connection_file(find_connection_file())
    return client


def requested_fields(reply, action, verbose):
    subfield = {'execute': reply['content'].get('user_expressions'),
                'complete': reply['content'].get('matches'),
                'inspect': reply['content'].get('data').get('text/plain')}
    return reply_content if verbose else subfield[action]


def main(action, code, verbose):
    client = client_connection_to_kernel()
    if action == 'execute':
        reply = getattr(client, action)(code, reply=True, allow_stdin=False)
    else:
        reply = getattr(client, action)(code, reply=True)
    fields = requested_fields(reply, action, verbose)
    print(fields)
    return fields


if __name__ == '__main__':
    kwargs = get_kwargs()
    main(**kwargs)
