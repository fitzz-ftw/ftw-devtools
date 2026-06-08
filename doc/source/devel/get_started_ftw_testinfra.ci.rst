.. _gs_TestHome_Environment:

Getting Started with TestHomeEnvironment
========================================

The ``TestHomeEnvironment`` is designed to create a safe, isolated sandbox for 
testing tools that interact with the user's home directory and configuration 
paths.

Setup the Environment
---------------------

First, we need to define a base directory for our test. In this example, 
we use a directory within our documentation structure.


>>> from pathlib import Path
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment

Define the anchor for our test environment

>>> base_path = Path("doc/source/devel/testhome")
>>> env = TestHomeEnvironment(base_path, appname="test")
>>> env.setup()
>>> env #doctest: +ELLIPSIS
TestHomeEnvironment(base_dir='...doc/source/devel/testhome')

>>> env.appname
'test'

>>> env.appname = 234
Traceback (most recent call last):
    ...
TypeError: Application name must be a string or None

>>> env.appname = "ftw"

>>> env.appauthor is None
True

>>> env.appauthor = 789
Traceback (most recent call last):
    ...
TypeError: Application author must be a string, bool, or None

>>> env.appauthor = False

>>> env.appauthor
False

>>> env.appauthor = True

>>> env.appauthor is None
True

>>> env.appauthor = "Big in Japan"

>>> env.appauthor
'Big in Japan'


This will give you a clean 'output' directory or CWD.
If you need the content of this directory, use

>>> env.setup(clean_output = False)

Understanding the Paths
-----------------------

After calling ``setup()``, the environment has prepared three main areas. 
Notice that the current working directory has automatically shifted to 
the ``output_dir``.


The current working directory is now the sandbox output

>>> Path.cwd() == env.output_dir
True

The 'testinput' directory is meant for static files from Git

>>> env.input_dir.name
'testinput'

Isolation from the System
-------------------------

The environment has redirected the ``HOME`` variable. Libraries like 
``platformdirs`` will now point into our ``base_path`` instead of your 
real user folder.

>>> import os
>>> os.environ['HOME'] == str(env.base_dir)
True

Using the intuitive HOME alias

>>> env.HOME == env.base_dir
True

To write to your HOME directory use:
>>> write_file = env.HOME / "testwrite.txt"

>>> _ = write_file.write_text("This is a test.")

>>> read_file = Path("~/testwrite.txt").expanduser()
>>> read_file.exists()
True

>>> read_file.read_text()
'This is a test.'

Deploying Configuration Files
-----------------------------

You can easily "inject" files from your static ``testinput`` into the 
simulated user configuration. Imagine you have a file named ``config_v1.toml`` 
in your ``testinput`` folder.

*(Note: For this test to run, the file must exist in the real filesystem)*

This copies: testhome/testinput/config_v1.toml 
to: testhome/.config/ftw/patch.toml (on Linux)
    
>>> target_path = env.copy2config("config_v1.toml", "patch.toml")
>>> target_path.as_posix() #doctest: +ELLIPSIS
'.../ftw/patch.toml'

Beside the ``config`` directory there are other user specific directories.

One is the shared data directory.

>>> shared_data = env.copy2data("test_data_file.txt")
>>> shared_data.as_posix()   #doctest: +ELLIPSIS 
'.../ftw/test_data_file.txt'

>>> shared_data.exists()
True

To clean the HOME directory you can use:

>>> env.clean_home()
>>> shared_data.exists()
False

And the user specific 'cache' directory:

>>> cached_file = env.copy2cache("test_cache_file.txt")

To prevent to do clening your HOME directory accidantly you can use:

>>> env.do_not_clean = True
>>> cached_file.exists()
True

>>> env.clean_home()
>>> cached_file.exists()
True

>>> env.do_not_clean
True

>>> env.do_not_clean = False

What happend if the file to copy does not exists:

>>> _ = env.copy2cache("non_existing_file.txt") #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
FileNotFoundError: Source file non_existing_file.txt not found in ...testinput

Copy Operations
----------------

There are two copy operations for use in these environment:

Copy from the 'input' director into the CWD.

>>> new_file = env.copy2cwd("testcopy.txt")
>>> new_renamed_file = env.copy2cwd("testcopy.txt", "copytest.txt")

>>> file_in_dir = env.copy2cwd("testcopy.txt", "new_dir/copytest.txt")

If the source file not exists:

>>> _ = env.copy2cwd("non_existing_file.txt") #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
FileNotFoundError: Source file non_existing_file.txt not found in ...testinput

And the other is to copy a file from CWD to another persistent directory
named 'testdocinc'. This directory should although be in the repository,
to enable showing file content in the build documentation.

>>> env.docinclude.as_posix() #doctest: +ELLIPSIS
'...doc/source/devel/testhome/testdocinc'

To copy a file to this directory use:

>>> saved_file = env.cwd2doc_inc("testcopy.txt", "saved_copy.txt")

If you try to save a file that is not there, maybe not written, you 
will get:

>>> _ = env.cwd2doc_inc("non_existing_file.txt", "saved_copy.txt") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Traceback (most recent call last):
    ...
FileNotFoundError: Source file for doc include not 
    found: ...non_existing_file.txt



Cleaning up
-----------

At the end of the doctest, we restore the original system state.

>>> env.teardown()

This will give you a clean 'output' directory or CWD.
If you need the content of this directory, use

>>> env.setup(clean_output = False)

>>> env.clean_output()

At the end of the doctest, we restore the original system state.

>>> env.teardown()
