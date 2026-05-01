# File: src/fitzzftw/devtools/git_shortcuts/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================

Main entry points for git shortcut utilities. (rw)
"""

import sys
from pathlib import Path

from fitzzftw.devtools.git_shortcuts.cli_parser import get_changelog_parser
from fitzzftw.devtools.git_shortcuts.git_commands import get_latest_tag, get_log_stat


# FUNCTION - prog_ftwchangelog
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
