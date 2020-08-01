# toju

A small CLI script for interacting with a Jupyter kernel from the command line.

---

## Installation

`toju` is a single, short Python script with no dependencies beyond the Python
standard library and `jupyter_client`, which is already in your environment if
you're looking to connect to a Jupyter kernel. 

<a id="make-executable"></a>On Unix-like systems, I recommend cloning this
repository, making `toju` executable, and adding a symbolic link to it in
/usr/local/bin. This will add `toju` to your system's `$PATH`, making it
available without needing to (explicitly) invoke `python`:

```bash
    $ git clone https://github.com/BrennanBarker/toju.git
    $ cd toju
    $ chmod +x toju.py
    $ ln -s <FULL-PATH-TO>/toju.py /usr/local/bin 
```

## Usage

`toju` sends code to a running Jupyter kernel for execution; by default, this
will be the most recently started kernel from any of the Jupyter frontends: the
in-terminal `jupyter console`, the independent GUI app `jupyter qtconsole`, a
`jupyter notebook`, or a notebook or console instance opened from `jupyter lab`.

Currently, `toju` works best with the Qt Console frontend, which will display
the output of code executions requested by `toju` when invoked with the
following option:

```bash
    $ jupyter qtconsole --JupyterWidget.include_other_output=True
```

You can also set this option permanently and adjust many other features by
setting up a config file per the [Qt Console
documentation](qtconsole.readthedocs.com).

You can certainly connect to a kernel started in a Jupyter Notebook or a
console within JupyterLab, but the output is not automatically displayed. You
can see that code sent by `toju` is still executed in the kernel, however, by 
executing code using `toju` and then running the Jupyter cell magic `%rerun`.

If you have just a single kernel running, simply invoke `toju` with the code
you'd like execute in the kernel as an argument. For example (assuming you have
made `toju` executable and placed it on your $PATH [as
above](#make-executable)):

```bash
    $ toju "print('Hello World')"
```

`toju` will send code passed to it from standard input, instead of arguments --
this is useful for piping in code from another shell command, reading from a
file, or for typing multi-line code blocks with here-document (<<). For
example:

```bash
    $ echo "print('Hello World')" | toju
```
```bash
    $ echo "print('Hello World')" > example.txt
    $ toju < example.txt
```
```bash
    $ toju << EOF
    heredoc> print('Hello')
    heredoc> print('World')
    heredoc> EOF
```

Accepting from standard input also allows `toju` to allow any programs with an
ability to access the shell to easily send code to a Jupyter kernel. For
example, in Vim, the following maps `<leader>J` to sending the current file (in
Normal mode) or selected lines (in Visual mode) to the most recently opened
Jupyter kernel:

```vim
    :noremap <silent> <leader>J :w !toju<cr><cr>
```

For those interested in a Vim plugin featuring many additional integrations
with Jupyter, consider [Jupyter-Vim](https://github.com/wmvanvliet/jupyter-vim).
