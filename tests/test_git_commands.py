import subprocess
from unittest.mock import MagicMock, patch

import pytest

from fitzzftw.devtools.git_shortcuts.git_commands import get_latest_tag, get_log_stat, run_git_command


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
