# File: src/fitzzftw/devtools/git_shortcuts/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================

This module provides tools to collect git information and code coverage data.

"""

import sys
from pathlib import Path

from fitzzftw.devtools.git_shortcuts.cli_parser import get_changelog_parser
from fitzzftw.devtools.git_shortcuts.git_commands import ProjektLogs, get_latest_tag, get_log_stat


# FUNCTION - prog_ftwchangelog may be deprecated
def prog_ftwchangelog(argv: list[str] | None = None) -> int:
    """
    Main entry point for the ftwchangelog tool. (rw)

    Generates a formatted git log since the last tag or a specific reference.
    """
    try:
        parser = get_changelog_parser()
        args = parser.parse_args(argv)

        start_ref = args.since if args.since else get_latest_tag(git_exec=args.git_path)

        log_data = get_log_stat(start_ref=start_ref, end_ref=args.branch, git_exec=args.git_path)

        print(f"--- Git Changes since {start_ref} ---")
        print(log_data)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

# !FUNCTION - prog_ftwchangelog

# FUNCTION - prog_commit_log
def prog_commit_log(argv: list[str] | None = None) -> int:
    """
    Create and save logs for git changes and code coverage.

    This function initializes a log manager to collect differences and
    coverage data across working directories. It handles errors and
    returns specific exit codes based on the outcome.

    :param argv: The list of arguments used to configure the log manager.
    :raises coverage.exceptions.NoDataError: If coverage information is missing.
    :raises OSError: If there are issues accessing directories or files.
    :raises Exception: For any other errors during the execution.
    :returns: A numeric code representing the success or failure status.
    """
    try:
        log = ProjektLogs(argv)
        log.run_diff()
        return 0
    except Exception as err:
        print(err)
        return 1
# !FUNCTION - prog_commit_log

# FUNCTION - prog_deploy_log
def prog_deploy_log(argv: list[str] | None = None) -> int:
    """
    Generate and save git history logs for all projects.

    This function uses the project log manager to collect git log data
    from the working directories. It returns a status code to indicate
    if the log creation was successful or if an error occurred.

    :param argv: The list of arguments for configuring the log manager.
    :raises OSError: If there are problems accessing the directories or files.
    :raises Exception: For any other errors during the log process.
    :returns: A numeric status code where 0 is success and 1 is an error.
    """
    try:
        log = ProjektLogs(argv)
        log.run_log()
        return 0
    except Exception as err:
        print(err)
        return 1
# !FUNCTION - prog_deploy_log


if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[4] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_git_sc_programms.rst"

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
