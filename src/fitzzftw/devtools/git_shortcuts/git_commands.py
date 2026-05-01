# File: src/fitzzftw/devtools/git_shortcuts/git_commands.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
git_commands
===============================

Low-level git command execution with flexible executable path. (rw)
"""

import subprocess
from pathlib import Path


# FUNCTION - run_git_command
def run_git_command(args: list[str], git_exec: str = "git") -> str:
    """
    Execute a git command and return the stripped stdout. (ro)

    :param args: List of command arguments.
    :param git_exec: Path to the git binary (validated by CLI parser).
    :return: The command output as a string.
    :raises RuntimeError: If the git command returns a non-zero exit code.
    """
    cmd = [git_exec] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() or str(e)
        raise RuntimeError(f"Git command failed: {error_msg}") from e


# !FUNCTION - run_git_command


# FUNCTION - get_latest_tag
def get_latest_tag(git_exec: str = "git") -> str:
    """
    Retrieve the latest git tag from the repository. (ro)

    :param git_exec: Path to the git binary.
    :return: The name of the most recent tag.
    """
    return run_git_command(["describe", "--tags", "--abbrev=0"], git_exec=git_exec)


# !FUNCTION - get_latest_tag


# FUNCTION - get_log_stat
def get_log_stat(start_ref: str, end_ref: str = "HEAD", git_exec: str = "git") -> str:
    """
    Get the git log with statistics between two references. (ro)

    :param start_ref: The starting tag or commit hash.
    :param end_ref: The end reference, defaults to "HEAD".
    :param git_exec: Path to the git binary.
    :return: The git log output including file statistics.
    """
    return run_git_command(["log", f"{start_ref}..{end_ref}", 
                            "--format=commit: %h %d%n%B"], git_exec=git_exec)


# !FUNCTION - get_log_stat


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
    test_file = testfiles_dir / "get_started_git_sc_git_commands.rst"

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
