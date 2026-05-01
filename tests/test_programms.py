from unittest.mock import MagicMock, patch

import pytest

from fitzzftw.devtools.git_shortcuts.programms import prog_ftwchangelog


def test_prog_ftwchangelog_success(capsys):
    """Verify successful changelog generation and output."""
    with (
        patch("fitzzftw.devtools.git_shortcuts.programms.get_changelog_parser") as mock_parser,
        patch("fitzzftw.devtools.git_shortcuts.programms.get_latest_tag") as mock_tag,
        patch("fitzzftw.devtools.git_shortcuts.programms.get_log_stat") as mock_log,
    ):
        # Mocking der Rückgabewerte
        mock_args = MagicMock()
        mock_args.since = None
        mock_args.branch = "main"
        mock_args.git_path = "git"
        mock_parser.return_value.parse_args.return_value = mock_args

        mock_tag.return_value = "v0.1.0"
        mock_log.return_value = "commit: 123abc\nUpdate README"

        exit_code = prog_ftwchangelog([])

        assert exit_code == 0
        out, _ = capsys.readouterr()
        assert "--- Git Changes since v0.1.0 ---" in out
        assert "commit: 123abc" in out


def test_prog_ftwchangelog_exception_handling(capsys):
    """Ensure 100% coverage by forcing an error in the main program loop."""
    with patch("fitzzftw.devtools.git_shortcuts.programms.get_changelog_parser") as mock_parser:
        mock_parser.side_effect = Exception("Unexpected CLI Error")

        exit_code = prog_ftwchangelog([])

        assert exit_code == 1
        _, err = capsys.readouterr()
        assert "Error: Unexpected CLI Error" in err
