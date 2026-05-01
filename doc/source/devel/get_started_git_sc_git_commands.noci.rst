.. _gs_GitCommands:

Getting Started with Git Commands
=================================

The ``git_commands`` module provides a wrapper to execute Git operations 
consistently and capture their output.

>>> from fitzzftw.devtools.git_shortcuts.git_commands import run_git_command

A simple command to check if we are in a work tree

>>> run_git_command(["rev-parse", "--is-inside-work-tree"])
'true'

If a command fails, it should raise a CalledProcessError (or your specific error handling)

>>> run_git_command(["invalid-command"]) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
RuntimeError: ...

To get the last git tag use :func:`get_latest_tag`.

>>> from fitzzftw.devtools.git_shortcuts.git_commands import get_latest_tag

>>> git_tag = get_latest_tag()
>>> type(git_tag) == str
True

To get the log entries you have to use

>>> from fitzzftw.devtools.git_shortcuts.git_commands import get_log_stat

>>> print(get_log_stat("v0.0.1", "v0.1.0")) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
commit: 7884a0f  (tag: v0.1.0, ...)
merge: development into main (v0.0.1)
<BLANKLINE>
Consolidate the initial development of ftw-devtools.
This merge establishes the project foundation as a Testing Infrastructure
Utility, including the 'TestHomeEnvironment' and full namespace integration.
<BLANKLINE>
Summary:
- Finalized PEP 420 namespace: fitzzftw.devtools
- Verified cross-python compatibility (3.11 - 3.15) via tox
- Completed documentation base and PyPI release readiness
<BLANKLINE>
commit: 491de60 
added v0.1.0 part
<BLANKLINE>
commit: 0e23503 
feat: add project documentation base
<BLANKLINE>
- Add README, CHANGELOG and index.rst



