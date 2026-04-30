# File: src/fitzzftw/devtools/git_shortcuts/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
cli_parser
===============================

CLI argument parsing with a robust base class for git tools. (rw)
"""

import shutil
import sys
from argparse import ArgumentError, ArgumentParser
from pathlib import Path
from typing import NoReturn, Sequence, cast

from fitzzftw.devtools.git_shortcuts.protocols import ChangelogCliProtocol, GitBaseCliProtocol


# CLASS - GitBaseParser
class GitBaseParser(ArgumentParser):
    """
    Base parser for all git-related tools. (rw)

    Provides the --git-path option and validates git availability.
    """

    # METHODE - __init__
    def __init__(self, *args, **kwargs):
        """
        Initialize the base parser with the 3.11-compatible safe init. (rw)
        """
        if len(args) < 3 and "description" not in kwargs:
            kwargs["description"] = "Git developer tool."
        kwargs["exit_on_error"] = False
        super().__init__(*args, **kwargs)
        self._setup_parser()

    # !METHODE - __init__
    # METHODE - _setup_parser
    def _setup_parser(self) -> None:
        """
        Define arguments common to all git tools. (rw)
        """
        self.add_argument(
            "--git-path",
            dest="git_path",
            type=str,
            help="Path to the git executable (defaults: %(default)s).",
            default="git",
        )

    # !METHODE - _setup_parser
    # METHODE - parse_args
    def parse_args(self, args: Sequence[str] | None = None, namespace=None) -> GitBaseCliProtocol:
        """
        Parse arguments and validate that git is available. (rw)
        """
        parsed_args = super().parse_args(args, namespace)

        # Validierung: Existiert git und ist es ausführbar?
        git_exec = parsed_args.git_path
        if not shutil.which(git_exec):
            self.error(f"Git executable '{git_exec}' not found or not executable.")

        return cast(GitBaseCliProtocol, parsed_args)

    # !METHODE - parse_args
    # METHODE - error
    def error(self, message) -> NoReturn:
        """
        Handle parsing errors by raising ArgumentError. (rw)

        :param message: The error message to report.
        :raises ArgumentError: Always raises to prevent SystemExit.
        """
        if sys.version_info[:2] == (3, 11):  # py 3.11 only no cover
            raise ArgumentError(None, message)
        super().error(message)  # not py 3.11 no·‌cover

    # !METHODE - error
    # METHODE - exit
    def exit(self, status=0, message=None) -> NoReturn:
        """
        Intercept exit calls to maintain control flow. (rw)

        :param status: Exit status code.
        :param message: Optional error message.
        """
        if sys.version_info[:2] == (3, 11) and status != 0:  # py 3.11 only no cover
            self.error(message or f"Exited with status {status}")
        super().exit(status, message)  # not py 3.11 no cover

    # !METHODE - exit


# !CLASS - GitBaseParser


# CLASS - ChangelogCliParser
class ChangelogCliParser(GitBaseParser):
    """
    Specialized parser for the ftwchangelog utility. (rw)
    """

    # METHODE - __init__
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize with a specific description for changelogs. (rw)
        """
        if len(args) < 3 and "description" not in kwargs:
            kwargs["description"] = "Generate git log statistics for changelogs."
        super().__init__(*args, **kwargs)

    # !METHODE - __init__
    # METHODE - _setup_parser
    def _setup_parser(self) -> None:
        """
        Extend base arguments with changelog-specific flags. (rw)
        """
        super()._setup_parser()
        self.add_argument(
            "-s",
            "--since",
            dest="since",
            type=str,
            default="last tag",
            help="Starting tag or commit hash (defaults: %(default)s).",
        )
        self.add_argument(
            "-b",
            "--branch",
            dest="branch",
            type=str,
            help="The branch or reference to compare (default: %(default)s).",
            default="development",
        )

    # !METHODE - _setup_parser
    # METHODE - parse_args

    def parse_args(self, args: Sequence[str] | None = None, namespace=None) -> ChangelogCliProtocol:
        """
        Parse and cast to the specific Changelog protocol. (rw)
        """
        ret = cast(ChangelogCliProtocol, super().parse_args(args, namespace))
        if ret.since == "last tag":
            ret.since =""
        return ret

    # !METHODE - parse_args


# !CLASS - ChangelogCliParser


# FUNCTION - get_changelog_parser
def get_changelog_parser() -> ChangelogCliParser:
    """
    Helper function to get a configured changelog parser instance. (rw)

    Note: This function is required by the sphinx-argparse extension
    to automatically generate CLI documentation.
    """
    return ChangelogCliParser()


# !FUNCTION - get_changelog_parser

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
    test_file = testfiles_dir / "get_started_cli_parser.rst"

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
