# File: src/fitzzftw/devtools/testinfra.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
testinfra
===============================


Modul testinfra documentation
"""

import os
import shutil
from pathlib import Path
from typing import Literal

from platformdirs import user_cache_path, user_config_path, user_data_path

# Future-proofing: pyfakefs will be used in TestRootEnvironment
# import pyfakefs.fake_filesystem_unittest as fake_fs


class TestHomeEnvironment:
    """
    Manages a physical test directory on the real filesystem.

    This class provides a sandbox by redirecting the user's HOME and
    related environment variables to a specific test directory. This
    isolates the developer's actual system from side effects during
    test execution.
    """

    def __init__(
        self,
        base_dir: str | Path,
        *,
        appname: str | None = None,
        appauthor: str | bool | None = None,
    ) -> None:
        """
        Initialize the environment paths.

        :param base_dir: Path to the directory acting as the test anchor.
        :param appname: Name of the application for path resolution.
        :param appauthor: Author of the application for path resolution.
        """
        self._base_dir = Path(base_dir).resolve()
        self._appname = appname
        self._appauthor: str | Literal[False] | None = None
        self.appauthor = appauthor
        self._input_dir = self._base_dir / "testinput"
        self._output_dir = self._base_dir / "testoutput"
        self._doc_inc = self._base_dir / "testdocinc"
        self._orig_cwd = Path.cwd()
        self._orig_env: dict[str, str] = {}
        self._do_not_clean = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base_dir='{self._base_dir.as_posix()}')"

    @property
    def docinclude(self) -> Path:
        """
        The path to the documentation include directory **(ro)**.

        :return: Path to the doc include folder.
        """
        return self._doc_inc

    @property
    def base_dir(self) -> Path:
        """
        The root of the test environment **(ro)**.

        :return: The base directory path.
        """
        return self._base_dir

    @property
    def HOME(self) -> Path:
        """
        Alias for base_dir to provide intuitive access to the simulated HOME **(ro)**.

        :return: The simulated HOME path.
        """
        return self.base_dir

    @property
    def realHOME(self)-> str:
        """
        Retrieve the real system HOME environment variable **(ro)**.

        :return: The path of the actual system HOME.
        """
        return os.environ['HOME']

    @property
    def in_env(self) -> bool:
        """
        Check if the current HOME matches the real system HOME **(ro)**.

        :return: True if in the system environment, False otherwise.
        """
        return self.HOME == self.realHOME

    @property
    def input_dir(self) -> Path:
        """
        Read-only directory containing Git-tracked test files **(ro)**.

        :return: The input directory path.
        """
        return self._input_dir

    @property
    def output_dir(self) -> Path:
        """
        Writable directory for test execution **(ro)**.

        :return: The output directory path.
        """
        return self._output_dir
    
    @property
    def doc_inc_dir(self)-> Path:
        """
        The path to the documentation include directory **(ro)**.

        :return: The documentation include directory path.
        """
        return self._doc_inc

    @property
    def config_dir(self)-> Path:
        """
        The platform-specific configuration directory for the application **(ro)**.

        :return: The configuration directory path.
        """
        return user_config_path(appname=self.appname, appauthor=self.appauthor)

    @property
    def data_dir(self)-> Path:
        """
        The platform-specific data directory for the application **(ro)**.

        :return: The data directory path.
        """
        return user_data_path(appname=self.appname, appauthor=self.appauthor)

    @property
    def do_not_clean(self) -> bool:
        """
        Toggle the automatic cleaning of the test directory (**rw**).

        :param value: The boolean state to enable or disable cleaning.
        :returns: The current state of the cleaning lock.
        """
        return self._do_not_clean

    @do_not_clean.setter
    def do_not_clean(self, value: bool) -> None:
        """
        Toggle the automatic cleaning of the test directory (**rw**).

        :param value: The boolean state to enable or disable cleaning.
        :returns: The current state of the cleaning lock.
        """
        self._do_not_clean = bool(value)

    @property
    def appname(self) -> str|None:
        """
        The name of the application used for path resolution **(rw)**.

        :param value: The new application name.
        :raises TypeError: If the provided value is not a string (Setter).
        :returns: The current application name.
        """
        return self._appname

    @appname.setter
    def appname(self, value: str | None) -> None:
        """
        The name of the application used for path resolution **(rw)**.

        :param value: The new application name.
        :raises TypeError: If the provided value is not a string (Setter).
        :returns: The current application name.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("Application name must be a string or None")
        self._appname = value

    @property
    def appauthor(self) -> str|Literal[False]|None:
        """
        The author of the application, critical for Windows path resolution **(rw)**.

        :param value: The new application author.
        :raises TypeError: If the provided value is not a string (Setter).
        :returns: The current application author.
        """
        return self._appauthor

    @appauthor.setter
    def appauthor(self, value: str | bool | None) -> None:
        """
        The author of the application, critical for Windows path resolution **(rw)**.

        :param value: The new application author.
        :raises TypeError: If the provided value is not a string (Setter).
        :returns: The current application author.
        """
        if value is not None and not isinstance(value, (str, bool)):
            raise TypeError("Application author must be a string, bool, or None")

        # Guard: Convert True to None to match platformdirs specifications
        if value is True:
            self._appauthor = None
        else:
            self._appauthor = value

    def setup(self, clean_output: bool = True) -> None:
        """
        Prepare the environment, redirect HOME, and switch to output_dir.

        :param clean_output: If True, existing output files are deleted.
        :raises OSError: If directories cannot be created or deleted.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.input_dir.mkdir(parents=True, exist_ok=True)

        if clean_output and self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        env_to_redirect = ["HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA"]
        env_to_neutralize = [
            "XDG_CONFIG_HOME",
            "XDG_DATA_HOME",
            "XDG_CACHE_HOME",
            "XDG_RUNTIME_DIR",
            "XDG_STATE_HOME",
        ]

        for var in env_to_redirect + env_to_neutralize:
            if var in os.environ:
                self._orig_env[var] = os.environ[var]

            if var in env_to_redirect:
                os.environ[var] = str(self.base_dir)
            else:
                if var in os.environ:
                    del os.environ[var]

        os.chdir(self.output_dir)

    def _copy_to_user_dir(
        self,
        app_name: str | None,
        source_name: str,
        target_name: str | None,
        get_path_func,
        *,
        app_author: str | Literal[False] | None = None,
    ) -> Path:
        """
        Internal helper for deploying files from testinput to user directories.

        :param app_name: Name of the application.
        :param source_name: Filename inside input_dir.
        :param target_name: Optional new name at the destination.
        :param get_path_func: Function to retrieve the target platform path.
        :param app_author: Author of the application (required for Windows).
        :raises FileNotFoundError: If the source file is missing in input_dir.
        :raises OSError: If the copy operation fails.
        :returns: The path to the newly created file.
        """
        source_path = self.input_dir / source_name
        if not source_path.exists():
            raise FileNotFoundError(f"Source file {source_name} not found in {self.input_dir}")

        # Use property as fallback if keyword argument is not provided
        author = app_author or self.appauthor
        appname = app_name or self.appname

        target_dir = get_path_func(appname=appname, appauthor=author)

        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / (target_name or source_name)

        shutil.copy2(source_path, target_path)
        return target_path

    def copy2config(self, source_name: str, target_name: str | None = None) -> Path:
        """
        Copy a file from testinput to the OS-specific user config directory.

        :param source_name: Filename inside input_dir.
        :param target_name: Optional new name at the destination.
        :raises FileNotFoundError: If the source file is missing.
        :returns: The path to the newly created configuration file.
        """
        return self._copy_to_user_dir(
            self.appname, source_name, target_name, user_config_path, app_author=self.appauthor
        )

    def copy2data(self, source_name: str, target_name: str | None = None) -> Path:
        """
        Copy a file from testinput to the OS-specific user data directory.

        :param source_name: Filename inside input_dir.
        :param target_name: Optional new name at the destination.
        :raises FileNotFoundError: If the source file is missing.
        :returns: The path to the newly created data file.
        """
        return self._copy_to_user_dir(
            self.appname, source_name, target_name, user_data_path, app_author=self.appauthor
        )

    def copy2cache(self, source_name: str, target_name: str | None = None) -> Path:
        """
        Copy a file from testinput to the OS-specific user cache directory.

        :param source_name: Filename inside input_dir.
        :param target_name: Optional new name at the destination.
        :raises FileNotFoundError: If the source file is missing.
        :returns: The path to the newly created cache file.
        """
        return self._copy_to_user_dir(
            self.appname, source_name, target_name, user_cache_path, app_author=self.appauthor
        )

    def copy2cwd(self, source_name: str, target_name: str | None = None) -> Path:
        """
        Copy a file from testinput directly to the current working directory.

        As setup() changes the CWD to output_dir, this method places files
        directly into the active test sandbox.

        :param source_name: Filename inside input_dir.
        :param target_name: Optional new name or relative path at the destination.
        :raises FileNotFoundError: If the source file is missing.
        :raises OSError: If the copy operation or directory creation fails.
        :returns: The path to the newly created file in the CWD.
        """
        source_path = self.input_dir / source_name
        if not source_path.exists():
            raise FileNotFoundError(f"Source file {source_name} not found in {self.input_dir}")

        target_path = Path.cwd() / (target_name or source_name)
        # Ensure all parent directories of the target path exist
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        return target_path

    def cwd2doc_inc(self, filename: str | Path, target_name: str | None = None) -> Path:
        """
        Copies a file from the current working directory (CWD) to the
        documentation includes directory (testdocinc).

        This allows persisting files generated during tests (like patches
        or configurations) for use in Sphinx documentation, even if the
        CWD is cleaned up later.

        :param filename: Name or path of the source file in the CWD.
        :param target_name: Optional new name or relative path at the destination.
        :raises FileNotFoundError: If the source file does not exist in the CWD.
        :raises OSError: If the copy operation or directory creation fails.
        :returns: The path to the copied file in the 'testdocinc' directory.
        """
        source = Path.cwd() / filename
        if not source.exists():
            raise FileNotFoundError(f"Source file for doc include not found: {source}")

        # Ensure the target directory exists
        self._doc_inc.mkdir(parents=True, exist_ok=True)

        target_filename = target_name if target_name else source.name
        target_path = self._doc_inc / target_filename
        # Ensure all parent directories of the target path exist
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_path)
        return target_path

    def teardown(self) -> None:
        """
        Restore the original environment variables and working directory.
        """
        os.chdir(self._orig_cwd)
        for var, value in self._orig_env.items():
            os.environ[var] = value

    def clean_home(self) -> None:
        """
        Remove all files and directories from the simulated HOME except testinput and testoutput.

        This method cleans the sandbox while preserving the static input files
        required for further tests. The cleaning process can be suppressed by
        setting the property **do_not_clean** to True. If the property is
        active, calling this method will have no effect on the file system.
        """
        if self.do_not_clean:
            return

        for item in self.base_dir.iterdir():
            if item == self.input_dir or item == self.docinclude:
                continue
            if item.is_dir() and item != self.output_dir:
                shutil.rmtree(item)
            elif item == self.output_dir:
                pass
            else:
                item.unlink()
    
    def clean_output(self) -> None:
        """
        Remove all files and directories from the testoutput directory.
        """
        for item in self.output_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()



if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_ftw_testinfra.ci.rst"

    if test_file.exists():
        print(f"--- Running Doctest for {test_file.name} ---")
        doctestresult = testfile(
            str(test_file),
            module_relative=False,
            verbose=be_verbose,
            optionflags=option_flags,
        )
        test_failed += doctestresult.failed
        test_sum += doctestresult.attempted
        if test_failed == 0:
            print(f"\nDocTests passed without errors, {test_sum} tests.")
        else:
            print(f"\nDocTests failed: {test_failed} tests.")
    else:
        print(f"⚠️ Warning: Test file {test_file.name} not found.")
