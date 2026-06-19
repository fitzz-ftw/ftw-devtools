# File: src/fitzzftw/devtools/git_shortcuts/git_commands.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
git_commands
===============================

Low-level git command execution with flexible executable path.
"""



import argparse
import io
import os
import subprocess
from datetime import datetime
from pathlib import Path

import coverage
from coverage.exceptions import NoDataError


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

def get_git_diff() -> str:
    """
    Get the current git diff output.

    :returns: The string containing the git diff data.
    """
    ret = subprocess.run(["git", "-P", "diff"], capture_output=True)
    return ret.stdout.decode("utf-8", errors="replace")

def get_git_log() -> str:
    """
    Combine different git log outputs into a single string.

    :returns: A formatted string containing git log history and file statuses.
    """
    ret1 = subprocess.run(
        ["git", "-P", "log", "--oneline", "--decorate", "--graph", "--all"],
        capture_output=True,
        text=True,
    )
    ret2 = subprocess.run(
        ["git", "-P", "log", "--name-status"],
        capture_output=True,
        text=True,
    )
    return "\n".join([ret1.stdout, ret2.stdout])

class ProjektLogs:
    """
    Manage project logs and output directories for reports.
    """

    def __init__(self, argv: list[str] | None = None) -> None:
        """
        Initialize the log manager and prepare output directories.

        :param argv: List of command line arguments for the parser.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "src_dest_dirs",
            type=Path,
            nargs="+",
            default=Path("."),
            metavar="<working-directory>",
            help="Directories to work in. (Default: %(default)s)",
        )
        parser.add_argument(
            "-o",
            "--output",
            "--output-dir",
            dest="output_dir",
            type=Path,
            default=None,
            help="Directory the output file is written. (Default: <working-directory>)",
        )
        args = parser.parse_args(argv)
        self._work_dirs = [d.resolve() for d in args.src_dest_dirs]
        self._old_path = Path().cwd()
        self._output_dir = None
        if args.output_dir is not None:
            self._output_dir = self._old_path / str(args.output_dir)
            self._output_dir = self._output_dir.resolve()
            if self._output_dir.is_dir() and any(self._output_dir.iterdir()):
                self._archive_dir = self._output_dir.with_name(
                    f"{self._output_dir.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                self._output_dir.rename(self._archive_dir)
            self._output_dir.mkdir(parents=True, exist_ok=True)

    def run_diff(self) -> None:
        """
        Create reports for git differences and coverage in all working directories.

        This method moves through each defined working directory to collect git
        changes and current code coverage results. It saves the combined data
        into a text file in the specified output directory or the local path.

        :raises coverage.exceptions.NoDataError: If coverage data is missing in a directory.
        :raises OSError: If changing directories or file writing fails.
        """
        for workdir in self._work_dirs:
            try:
                os.chdir(workdir)
                diff_content: str = get_git_diff()
                percentage = get_total_coverage()
                out_file_str = (
                    workdir.name
                    # workdir.name.split("-")[-1]
                    if workdir.name != ""
                    else Path(".").absolute().name
                    # else Path(".").absolute().name.split("-")[-1]
                )
                out_file = Path("-".join(["git", "diff", out_file_str])).with_suffix(".txt")
                out_file = out_file if self._output_dir is None else self._output_dir / out_file
                if not diff_content.strip():
                    print(
                        f"No Changes, did not create: "
                        f"{out_file.absolute().relative_to(self._old_path)}"
                    )
                    continue
                with out_file.open("w") as f:
                    print(f"Total-Coverage: {percentage:.2f}%", file=f)
                    print("-" * 20, "diff", "-" * 20, file=f)
                    print(diff_content, file=f)
                    print(f"Created: {out_file.absolute().relative_to(self._old_path)}")
            finally:
                os.chdir(self._old_path)

    def run_log(self) -> None:
        """
        Create reports for git history in all working directories.

        This method visits each working directory to collect git log
        information. It saves the combined history into a text file
        in the specified output directory or the current path.

        :raises OSError: If changing directories or writing the log file fails.
        """
        for workdir in self._work_dirs:
            try:
                os.chdir(workdir)
                log_content: str = get_git_log()
                out_file_str = workdir.name if workdir.name != "" else Path(".").absolute().name
                out_file = Path("-".join(["git", "log", out_file_str])).with_suffix(".txt")
                out_file = out_file if self._output_dir is None else self._output_dir / out_file
                if not log_content.strip():
                    print(
                        f"No Changes, did not create: "
                        f"{out_file.absolute().relative_to(self._old_path)}"
                    )
                    continue
                with out_file.open("w") as f:
                    print(log_content, file=f)
                    print(f"Created: {out_file.absolute().relative_to(self._old_path)}")
            finally:
                os.chdir(self._old_path)

def get_total_coverage() -> float:
    """
    Calculate the total code coverage percentage.

    :raises coverage.exceptions.NoDataError: If no coverage data file is found.
    :returns: The total percentage of code coverage or a negative value on error.
    """
    cov = coverage.Coverage()
    cov.load()
    null_out = io.StringIO()
    try:
        total_percentage = cov.report(output_format="total", file=null_out)
        return total_percentage
    except NoDataError:
        print("No coverage data found.\nPlease run coverage first.")
        return -0.1


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
    test_file = testfiles_dir / "get_started_git_sc_git_commands.noci.rst"

    if test_file.exists():
        print(f"--- Running Doctest for {test_file.name} ---")
        doctestresult = testfile(
            str(test_file),
            module_relative=False,
            verbose=be_verbose,
            optionflags=option_flags,
            globs={"nocovrun":True},
        )
        test_failed += doctestresult.failed
        test_sum += doctestresult.attempted
        if test_failed == 0:
            print(f"\nDocTests passed without errors, {test_sum} tests.")
        else:
            print(f"\nDocTests failed: {test_failed} tests.")
    else:
        print(f"⚠️ Warning: Test file {test_file.name} not found.")
