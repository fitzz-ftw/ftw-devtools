# File: src/fitzzftw/devtools/doctest_utils.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
doctest_utils
===============================


Modul doctest_utils documentation
"""
import shutil
import sys
from pathlib import Path


def dtprint(*entries: object, **printkw) -> None:
    """
    Print entries to stderr with a forced flush and standardized format.

    This function bypasses standard stdout and ignores 'file' or 'flush'
    arguments passed in kwargs to ensure output always goes to stderr.

    :param entries: Objects to be printed.
    :param printkw: Standard print function keyword arguments (file and flush are ignored).
    """
    printkw.pop("file", None)
    printkw.pop("flush", None)
    print(*entries, **printkw, file=sys.stderr, flush=True)

class NotVerbosePrint:
    """
    Callable class that suppresses output if the verbose flag is set to True.

    
    :ivar _verbose: If True, all output calls are ignored.
                         If False, output is redirected to stderr.
    """
    def __init__(self, verbose: bool) -> None:
        """
        Initialize the printer.

        :param verbose: Set to True to mute output.
        """
        self._verbose = verbose

    def __call__(self, *value: object, **printkw) -> None:
        """
        Print the provided values to stderr if verbose mode is disabled.

        :param *value: Objects to be printed.
        :param **printkw: Standard print function keyword arguments (file and flush are ignored).
        """
        if not self._verbose:
            dtprint(*value, **printkw)

class TestArtifactCollector:
    """Collects and exports test artifacts to a safe location outside HOME."""

    def __init__(self, base_export_dir:str| Path, clean_dir:bool=True):
        self.export_root = Path(base_export_dir).resolve()
        if clean_dir:
            self._clean_dir()
        # Stelle sicher, dass das Zielverzeichnis existiert
        self.export_root.mkdir(parents=True, exist_ok=True)

    @property
    def base_dir(self) -> Path:
        return self.export_root

    def _clean_dir(self):
        if self.export_root.exists() and self.export_root.is_dir():
            for entry in self.export_root.iterdir():
                shutil.rmtree(entry) if entry.is_dir() else entry.unlink()

    def export(self, source_file: Path|str, target_subdir: str) -> Path:
        """Copies a file to an external directory and returns the new path."""
        source_file = Path(source_file)
        dest_dir = self.export_root / target_subdir
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / source_file.name
        shutil.copy2(source_file, dest_path)
        return dest_path

    def __call__(self, source_file: Path | str, target_subdir: str) -> None:
        self.export(source_file, target_subdir)

if __name__ == "__main__": # pragma: no cover
    from doctest import FAIL_FAST, testfile
    
    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "get_started_doctest_utils.ci.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
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
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(f"\nKeep going! You already passed {passed_files} files "
                  f"with {test_sum} tests before this hit.")                
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
