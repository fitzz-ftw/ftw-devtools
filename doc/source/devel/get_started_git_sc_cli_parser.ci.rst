.. _gs_GitCliParser:

Getting Started with Git CLI Parser
===================================

In moment there are 2 parsers availible.

The first is the :class:`GitBaseParser`, all other parsers should be
derived from this one, it provides the check that the git exicutible is in the 
PATH. otherwise there is an option to specificate the path to the exicutible.

>>> from fitzzftw.devtools.git_shortcuts.cli_parser import GitBaseParser
>>> base_parser = GitBaseParser()

>>> base_parser.print_help() # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
usage: ... [-h] [--git-path GIT_PATH]
<BLANKLINE>
Git developer tool.
<BLANKLINE>
options:
    -h, --help           show this help message and exit
    --git-path GIT_PATH  Path to the git executable (defaults: git).

What do you see when you do not have a git executable in your PATH or 
you gave a wrong path to ``--git-path``:

>>> base_parser.parse_args(['--git-path', '/wrongpath/git'])
Traceback (most recent call last):
    ...
argparse.ArgumentError: Git executable '/wrongpath/git' not found or not executable.


For the ``ftwchangelog`` programm the following parser is used.

>>> from fitzzftw.devtools.git_shortcuts.cli_parser import ChangelogCliParser
>>> parser = ChangelogCliParser()
>>> parser #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
ChangelogCliParser(prog='...', 
    usage=None, 
    description='Generate git log statistics for changelogs.', 
    formatter_class=<class 'argparse...HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)



>>> parser.print_help() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
usage: ... [-h] [--git-path GIT_PATH] [-s SINCE] [-b BRANCH]
<BLANKLINE>
Generate git log statistics for changelogs.
<BLANKLINE>
options:...

The default value for the since argument is "last tag" for the help string.
It will be converted to an empty string ''.

>>> args = parser.parse_args([])
>>> args.since
''

If you set the option,

>>> args= parser.parse_args(["-s", "v9.2.1"])
>>> args.since
'v9.2.1'

it will returns as aspected.


To give the parser another description just call it like

>>> ChangelogCliParser(description="An other description").print_help() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
usage: ... [-h] [--git-path GIT_PATH] [-s SINCE] [-b BRANCH]
<BLANKLINE>
An other description
<BLANKLINE>
options:...


There is although a function in this module, which is called 
:func:`get_changelog_parser` which returns an instance of 
:class:`ChangelogCliParser`. It is mainly used by the Sphinx argparse extention.
If you like factory functions just use it.

>>> from fitzzftw.devtools.git_shortcuts.cli_parser import get_changelog_parser

>>> get_changelog_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
ChangelogCliParser(prog='...', 
    usage=None, 
    description='Generate git log statistics for changelogs.', 
    formatter_class=<class 'argparse...HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)
