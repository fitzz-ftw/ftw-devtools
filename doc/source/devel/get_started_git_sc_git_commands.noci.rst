.. _gs_GitCommands:

>>> nocovrun = globals().get("nocovrun", False)

>> nocovrun
>>> import fitzzftw.devtools.git_shortcuts.git_commands as g_c

.. import get_total_coverage


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
commit: 7884a0f  (tag: v0.1.0...)
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


>>> from fitzzftw.devtools.git_shortcuts.git_commands import get_git_diff

>>> get_git_diff() #doctest: +ELLIPSIS
'...



>>> from pathlib import Path
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment

Define the anchor for our test environment

>>> def stub_coverage():
...    return 80

>>> g_c.get_total_coverage = stub_coverage  if not nocovrun else g_c.get_total_coverage

>>> from fitzzftw.devtools.git_shortcuts.git_commands import get_total_coverage


>>> tc = get_total_coverage()  #if nocovrun else 80

>>> tc > 50
True


>>> from fitzzftw.devtools.git_shortcuts.git_commands import get_git_log

>>> get_git_log() #doctest: +ELLIPSIS
'...tag:...'

>>> from fitzzftw.devtools.git_shortcuts.git_commands import ProjektLogs

>>> pl=ProjektLogs([".", "-o", "doc/source/devel/testhome/testoutput"])

>>> pl.run_diff() # doctest: +ELLIPSIS
Created: ...git-diff-ftw-devtools.txt

>>> pl.run_log() # doctest: +ELLIPSIS
Created: ...git-log-ftw-devtools.txt

>>> pl2=ProjektLogs([".", "-o", "doc/source/devel/testhome/testoutput"])
>>> pl3=ProjektLogs([".", ])

>>> del pl2
>>> del pl3

>>> def stub_no_content():
...     return ""

>>> g_c.get_git_diff = stub_no_content

>>> pl.run_diff() # doctest: +ELLIPSIS
No Changes, did not create: ...git-diff-ftw-devtools.txt

>>> g_c.get_git_log = stub_no_content

>>> pl.run_log() # doctest: +ELLIPSIS
No Changes, did not create: ...git-log-ftw-devtools.txt
