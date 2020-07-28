import argparse
import sys
import jupyter_client




def create_client_connection_to_kernel():
    connection_file = jupyter_client.find_connection_file()
    client = jupyter_client.BlockingKernelClient()
    client.load_connection_file(connection_file)
    return client


if __name__ == '__main__':
    
    # Command-Line Interface
    arg_parser = argparse.ArgumentParser(
            prog='2QuTe',
            description='Interact with a Jupyter kernel from the command line')

    arg_parser.add_argument('code', action='store', nargs='?',
            default=sys.stdin)

    action_group = arg_parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-e', '--execute', action='store_true')
    action_group.add_argument('-c', '--complete', action='store_true')
    action_group.add_argument('-i', '--inspect', action='store_true')

    args = vars(arg_parser.parse_args()) 

    if type(args['code']) is not str:
        try:
            args['code'] = args['code'].read()
        except AttributeError:
            raise TypeError('Input is not a string, stdin, or file')

    # QT Messaging
    client = create_client_connection_to_kernel()

    if args['execute']:
        client.execute(args['code'])

    elif args['inspect']:
        client.inspect(args['code'], reply=True)
        print(reply['content']['data'])

    elif args['complete']:
        reply = client.complete(args['code'], reply=True)
        print(reply['content']['matches'])
