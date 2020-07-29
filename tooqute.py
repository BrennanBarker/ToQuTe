from argparse import ArgumentParser
import sys
from jupyter_client import find_connection_file, BlockingKernelClient

# TODO: verbose--get additional reply fields
# TODO: subcommmands vice choices
# TODO: check, respond with message status
# TODO: add better help


def get_kwargs():
    arg_parser = ArgumentParser(prog='tooqute',
            description='Interact with a Jupyter kernel from the command line')
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
    reply_content_fields = {'execute': 'user_expressions',
                            'complete': 'matches',
                            'inspect': 'data'}
    field = reply_content_fields[action]
    return reply['content'] if verbose else reply['content'][field]


def message_jupyter(client, action, code, verbose):
    reply = getattr(client, action)(code, reply=True)
    return requested_fields(reply, action, verbose)


def main(action, code, verbose):
    client = client_connection_to_kernel()
    reply = message_jupyter(client, action, code, verbose)
    print(reply if reply else 'Code sent to kernel.')


if __name__ == '__main__':
    kwargs = get_kwargs()
    main(**kwargs)
