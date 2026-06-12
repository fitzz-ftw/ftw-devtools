# Erstellt ein 'git diff' mit vorangestelltem Header mit
# Coverageangabe
import argparse
import io
import os
import subprocess
from datetime import datetime
from pathlib import Path

import coverage
from coverage.exceptions import NoDataError


def get_git_diff() -> str:
    ret = subprocess.run(["git", "-P", "diff"], capture_output=True, text=True)
    return str(ret.stdout)


def get_total_coverage():
    # Lädt die .coverage Datei aus dem aktuellen Verzeichnis
    cov = coverage.Coverage()
    cov.load()
    null_out = io.StringIO()
    # Berechnet die Gesamt-Coverage über alle Dateien hinweg
    # report() gibt den Wert zurück und schreibt ihn in die Konsole
    try:
        total_percentage = cov.report(output_format="total", file=null_out)
        return total_percentage
    except NoDataError:
        print("No coverage data found.\nPlease run coverage first.")
        return -0.1


# ('--pretty=format:"%h %s"',)


def get_git_log():
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
    def __init__(self, argv: list[str] | None = None) -> None:
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
        self._work_dirs = args.src_dest_dirs
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

    def run_diff(self):
        for workdir in self._work_dirs:
            try:
                os.chdir(workdir)
                diff_content: str = get_git_diff()
                percentage = get_total_coverage()
                out_file_str = (
                    workdir.name.split("-")[-1]
                    if workdir.name != ""
                    else Path(".").absolute().name.split("-")[-1]
                )
                out_file = Path("-".join(["git", "diff", out_file_str])).with_suffix(".txt")
                out_file = out_file if self._output_dir is None else self._output_dir / out_file
                if not diff_content.strip():
                    print(f"No Changes, did not create: {out_file.relative_to(self._old_path)}")
                    continue
                with out_file.open("w") as f:
                    print(f"Total-Coverage: {percentage:.2f}%", file=f)
                    print("-" * 20, "diff", "-" * 20, file=f)
                    print(diff_content, file=f)
                    print(f"Created: {out_file.absolute().relative_to(self._old_path)}")
            finally:
                os.chdir(self._old_path)

    def run_log(self):
        for workdir in self._work_dirs:
            try:
                os.chdir(workdir)
                log_content: str = get_git_log()
                out_file_str = (
                    workdir.name.split("-")[-1]
                    if workdir.name != ""
                    else Path(".").absolute().name.split("-")[-1]
                )
                out_file = Path("-".join(["git", "log", out_file_str])).with_suffix(".txt")
                out_file = out_file if self._output_dir is None else self._output_dir / out_file
                if not log_content.strip():
                    print(f"No Changes, did not create: {out_file.relative_to(self._old_path)}")
                    continue
                with out_file.open("w") as f:
                    print(log_content, file=f)
                    print(f"Created: {out_file.absolute().relative_to(self._old_path)}")
            finally:
                os.chdir(self._old_path)


def prog_commit_log(argv: list[str] | None = None) -> int:
    log = ProjektLogs(argv)
    log.run_diff()
    return 0


def prog_deploy_log(argv: list[str] | None = None) -> int:
    log = ProjektLogs(argv)
    log.run_log()
    return 0


if __name__ == "__main__":
    # prog_commit_log()
    prog_deploy_log()
