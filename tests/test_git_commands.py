import subprocess
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from coverage.exceptions import NoDataError

from fitzzftw.devtools.git_shortcuts.git_commands import (
    ProjektLogs,
    get_git_diff,
    get_git_log,
    get_latest_tag,
    get_log_stat,
    get_total_coverage,
    run_git_command,
)


def test_get_latest_tag_success() -> None:
    """Check if get_latest_tag returns the stripped output of git describe."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.run_git_command") as mock_run:
        mock_run.return_value = "v0.1.0"
        assert get_latest_tag() == "v0.1.0"
        mock_run.assert_called_with(["describe", "--tags", "--abbrev=0"], git_exec="git")


def test_get_latest_tag_failure() -> None:
    """Ensure RuntimeError is raised when git describe fails."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.run_git_command") as mock_run:
        mock_run.side_effect = RuntimeError("Git command failed")
        with pytest.raises(RuntimeError, match="Git command failed"):
            get_latest_tag()


def test_get_log_stat_format() -> None:
    """Verify that get_log_stat uses the correct git log format strings."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.run_git_command") as mock_run:
        get_log_stat("v0.1.0", "HEAD")
        args, _ = mock_run.call_args
        # Überprüfung, ob das spezifische Format-Flag übergeben wurde
        assert "--format=commit: %h %d%n%B" in args[0]

def test_run_git_command_called_process_error():
    """Verify that CalledProcessError is caught and re-raised as RuntimeError with stderr."""
    # Wir mocken subprocess.run, um einen Fehler zu werfen
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.subprocess.run") as mock_run:
        # Erstelle ein Mock-Objekt für den Fehler mit gefülltem stderr
        mock_error = subprocess.CalledProcessError(
            returncode=128, cmd=["git", "status"], stderr="fatal: not a git repository"
        )
        mock_run.side_effect = mock_error

        with pytest.raises(RuntimeError) as exc_info:
            run_git_command(["status"])

        # Prüfen, ob die Fehlermeldung korrekt extrahiert wurde
        assert "Git command failed: fatal: not a git repository" in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, subprocess.CalledProcessError)

def test_run_git_command_generic_exception():
    """Verify handling when stderr is empty."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.subprocess.run") as mock_run:
        mock_error = subprocess.CalledProcessError(returncode=1, cmd=["git", "status"])
        mock_error.stderr = ""  # Simuliere leeren stderr
        mock_run.side_effect = mock_error

        with pytest.raises(RuntimeError) as exc_info:
            run_git_command(["status"])

        # Hier sollte str(e) als Fallback genutzt werden
        assert "Command '['git', 'status']' returned non-zero exit status 1" in str(exc_info.value)

def test_run_git_command_success():
    """Verify that run_git_command returns stripped stdout on success."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.subprocess.run") as mock_run:
        # Simuliere ein erfolgreiches Result-Objekt
        mock_result = MagicMock()
        mock_result.stdout = "  some git output  \n"
        mock_run.return_value = mock_result

        from fitzzftw.devtools.git_shortcuts.git_commands import run_git_command

        result = run_git_command(["rev-parse", "HEAD"])

        assert result == "some git output"
        mock_run.assert_called_once()

def test_get_git_diff_success():
    """Verify that get_git_diff returns the decoded stdout."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.subprocess.run") as mock_run:
        # Mock-Result konfigurieren
        mock_result = MagicMock()
        mock_result.stdout = b"diff --git a/file b/file\nindex 123..456\n"
        mock_run.return_value = mock_result

        output = get_git_diff()

        assert output == "diff --git a/file b/file\nindex 123..456\n"
        mock_run.assert_called_once_with(["git", "-P", "diff"], capture_output=True)


def test_get_git_diff_encoding_error():
    """Verify that decoding errors are handled (e.g., binary noise)."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.subprocess.run") as mock_run:
        # Simuliere Binärdaten, die nicht sauber UTF-8 sind
        mock_result = MagicMock()
        mock_result.stdout = b"\xff\xfe\xfd"
        mock_run.return_value = mock_result

        output = get_git_diff()

        # 'replace' sorgt dafür, dass die Funktion nicht crasht
        assert isinstance(output, str)
        assert "\ufffd" in output  # Das Ersatzzeichen für ungültige Sequenzen

def test_get_git_log_success():
    """Verify that get_git_log combines outputs from two different log commands."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.subprocess.run") as mock_run:
        # Wir definieren zwei unterschiedliche Rückgabewerte für die zwei Aufrufe
        mock_log_graph = MagicMock()
        mock_log_graph.stdout = "* 123456 (HEAD) Commit message"

        mock_log_status = MagicMock()
        mock_log_status.stdout = "M\tfile.py"

        # side_effect erlaubt es, mehrere Aufrufe nacheinander zu "füttern"
        mock_run.side_effect = [mock_log_graph, mock_log_status]

        result = get_git_log()

        # Überprüfung der Kombination
        assert result == "* 123456 (HEAD) Commit message\nM\tfile.py"

        # Sicherstellen, dass beide Aufrufe korrekt getätigt wurden
        assert mock_run.call_count == 2

        # Prüfung der Argumente des ersten Aufrufs
        mock_run.assert_any_call(
            ["git", "-P", "log", "--oneline", "--decorate", "--graph", "--all"],
            capture_output=True,
            text=True,
        )
        # Prüfung der Argumente des zweiten Aufrufs
        mock_run.assert_any_call(
            ["git", "-P", "log", "--name-status"],
            capture_output=True,
            text=True,
        )

def test_get_total_coverage_success():
    """Verify that get_total_coverage returns the correct percentage."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.coverage.Coverage") as mock_cov_class:
        # Mock-Instanz erstellen
        mock_cov_instance = MagicMock()
        mock_cov_class.return_value = mock_cov_instance

        # Simuliere, dass report() 95.5 zurückgibt
        mock_cov_instance.report.return_value = 95.5

        result = get_total_coverage()

        assert result == 95.5
        mock_cov_instance.load.assert_called_once()
        mock_cov_instance.report.assert_called_once()


def test_get_total_coverage_no_data_error(capsys):
    """Verify that NoDataError is caught and returns -0.1."""
    with patch("fitzzftw.devtools.git_shortcuts.git_commands.coverage.Coverage") as mock_cov_class:
        mock_cov_instance = MagicMock()
        mock_cov_class.return_value = mock_cov_instance

        # Simuliere das Auslösen der Exception
        mock_cov_instance.report.side_effect = NoDataError("No data")

        result = get_total_coverage()

        assert result == -0.1

        # Prüfen, ob die Warnung auf stdout gelandet ist
        out, _ = capsys.readouterr()
        assert "No coverage data found" in out

def test_projektlogs_run_diff_success():
    """Testet den Happy-Path von run_diff unter kompletter Isolation."""
    # Mocks für Dateisystem und externe Aufrufe
    with (
        patch("os.chdir"),
        patch(
            "fitzzftw.devtools.git_shortcuts.git_commands.get_git_diff", return_value="some diff"
        ),
        patch(
            "fitzzftw.devtools.git_shortcuts.git_commands.get_total_coverage",
            return_value=99.0,
        ),
        patch("pathlib.Path.open", mock_open()) as mocked_file,
        patch("pathlib.Path.mkdir"),  # Verhindert echtes Erstellen von Dirs
    ):
        # Initialisierung mit einem Dummy-Pfad
        pl = ProjektLogs(argv=["."])
        pl.run_diff()

        # Sicherstellen, dass in die Datei geschrieben wurde
        mocked_file().write.assert_any_call("Total-Coverage: 99.00%")
        mocked_file().write.assert_any_call("\n")
        mocked_file().write.assert_any_call("some diff")

def test_projektlogs_init_archiving() -> None:
    """Testet den Archivierungs-Zweig (rename/mkdir) in der __init__."""
    with (
        patch("pathlib.Path.is_dir", return_value=True),
        patch("pathlib.Path.iterdir", return_value=[Path("dummy")]),  # Ordner ist nicht leer
        patch("pathlib.Path.rename") as mock_rename,
        patch("pathlib.Path.mkdir"),
    ):
        # Wir zwingen die __init__ in den Archivierungs-Block
        _ = ProjektLogs(argv=[".", "--output", "test_out"])
        assert mock_rename.called


def test_projektlogs_run_log_success():
    """Testet den Happy-Path von run_log."""
    mock_file = mock_open()
    with (
        patch("os.chdir"),
        patch(
            "fitzzftw.devtools.git_shortcuts.git_commands.get_git_log", return_value="some log history"
        ),
        patch("pathlib.Path.open", mock_file),
        patch("pathlib.Path.mkdir"),
    ):
        pl = ProjektLogs(argv=["."])
        pl.run_log()

        # Sicherstellen, dass das Log korrekt geschrieben wurde
        mock_file().write.assert_any_call("some log history")
        mock_file().write.assert_any_call("\n")


def test_projektlogs_run_log_no_content():
    """Testet den Branch, falls das Log leer ist (kein Dateischreib-Vorgang)."""
    with (
        patch("os.chdir"),
        patch(
            "fitzzftw.devtools.git_shortcuts.git_commands.get_git_log", return_value="  "
        ),  # Leerstring/Whitespace
        patch("pathlib.Path.open", mock_open()) as mock_file,
    ):
        pl = ProjektLogs(argv=["."])
        pl.run_log()

        # Wenn der String leer ist, darf write() nicht aufgerufen worden sein
        assert not mock_file().write.called

def test_projektlogs_run_diff_empty_diff():
    """Erzwingt den Sprung in den 'No Changes'-Zweig."""
    with (
        patch("os.chdir"),
        patch(
            "fitzzftw.devtools.git_shortcuts.git_commands.get_git_diff", return_value="  "
        ),  # Leer
        patch("pathlib.Path.open", mock_open()) as mocked_file,
    ):
        pl = ProjektLogs(argv=["."])
        pl.run_diff()
        # Sicherstellen, dass nichts geschrieben wurde (write darf nicht aufgerufen sein)
        assert not mocked_file().write.called

def test_projektlogs_init_archiving_branch_taken():
    """
    Dieser Test zwingt die Maschine in den Archivierungs-Block.
    """
    with (
        # is_dir muss True sein
        patch("pathlib.Path.is_dir", return_value=True),
        # iterdir muss einen Inhalt liefern, damit any(...) True ergibt
        patch("pathlib.Path.iterdir", return_value=[Path("irgendwas.txt")]),
        patch("pathlib.Path.rename") as mock_rename,
        patch("pathlib.Path.mkdir"),
    ):
        # Jetzt MUSS die Maschine in das if-Statement (139-142) springen
        _ = ProjektLogs(argv=[".", "--output", "test_output"])

        # Die Assertion beweist: Der Branch wurde genommen
        assert mock_rename.called

def test_projektlogs_run_diff_no_output_dir():
    """Testet den Pfad, wenn kein --output angegeben wurde (nutzt lokales Verzeichnis)."""
    with (
        patch("os.chdir"),
        patch(
            "fitzzftw.devtools.git_shortcuts.git_commands.get_git_diff", return_value="some diff"
        ),
        patch("fitzzftw.devtools.git_shortcuts.git_commands.get_total_coverage", return_value=90.0),
        patch("pathlib.Path.open", mock_open()) as mocked_file,
    ):
        # Initialisierung ohne -o
        pl = ProjektLogs(argv=["."])
        pl._output_dir = None  # Explizit auf None setzen, um den Branch zu erzwingen
        pl.run_diff()

        # Prüfen, ob in das lokale Verzeichnis geschrieben wurde
        assert mocked_file.called


def test_projektlogs_run_log_with_output_dir():
    """Testet den Pfad, wenn ein --output Verzeichnis gesetzt ist."""
    with (
        patch("os.chdir"),
        patch("fitzzftw.devtools.git_shortcuts.git_commands.get_git_log", return_value="log"),
        patch("pathlib.Path.open", mock_open()) as mocked_file,
        patch("pathlib.Path.mkdir"),
    ):
        pl = ProjektLogs(argv=[".", "--output", "custom_dir"])
        pl.run_log()

        # Prüfen, ob der Pfad unter custom_dir konstruiert wurde
        assert mocked_file.called
