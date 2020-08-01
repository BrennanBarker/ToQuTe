#! /usr/bin/env python
"""Send code to a Jupyter kernel from the command line."""

# TODO: option for different command separators for different languages?

import sys
from jupyter_client import find_connection_file, BlockingKernelClient


def main():
    client = BlockingKernelClient()
    client.load_connection_file(find_connection_file())
    code = "; ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    client.execute(code, allow_stdin=False)


if __name__ == '__main__':
    main()
