Git Programms Execution
=======================

Check the basic execution and output format of the ftwchangelog programm.

First we build the commandline.

>>> cmd_line="ftwchangelog -b main -s v0.0.1"

>>> import shlex 

>>> sys_argv = shlex.split(cmd_line)[1:]

>>> sys_argv
['-b', 'main', '-s', 'v0.0.1']

>>> from fitzzftw.devtools.git_shortcuts.programms import prog_ftwchangelog

>>> prog_ftwchangelog(sys_argv) #doctest: +ELLIPSIS
--- Git Changes since v0.0.1 ---
commit:...

>>> cmd_line="ftwchangelog -b main -s v0.0.1 --git-path /home/git"


>>> sys_argv = shlex.split(cmd_line)[1:]

>>> prog_ftwchangelog(sys_argv)
1

