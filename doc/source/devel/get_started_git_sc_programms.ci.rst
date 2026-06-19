New Git Programms Execution
=============================

>>> import fitzzftw.devtools.git_shortcuts.git_commands as g_c

Check the basic execution and output format of the ftwchangelog programm.

First we build the commandline.

>>> def stub_runner(*args):
...     return None

>>> def stub_exception(*args):
...     raise Exception("This is a test exception.")


>>> old_runlog = g_c.ProjektLogs.run_log
>>> old_rundiff= g_c.ProjektLogs.run_diff

>>> g_c.ProjektLogs.run_log = stub_runner
>>> g_c.ProjektLogs.run_diff = stub_runner

>>> from fitzzftw.devtools.git_shortcuts.programms import prog_deploy_log
>>> from fitzzftw.devtools.git_shortcuts.programms import prog_commit_log

>>> sys_argv = ["src_dest_dirs"]

>>> prog_deploy_log(sys_argv)
0

>>> prog_commit_log(sys_argv) 
0

>>> g_c.ProjektLogs.run_log = stub_exception
>>> g_c.ProjektLogs.run_diff = stub_exception

>>> prog_deploy_log(sys_argv)
This is a test exception.
1

>>> prog_commit_log(sys_argv) 
This is a test exception.
1



>>> g_c.ProjektLogs.run_log = old_runlog
>>> g_c.ProjektLogs.run_diff = old_rundiff
