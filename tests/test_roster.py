from pathlib import Path

import pytest

from greetings.cli import main
from greetings.roster import load_roster, process_roster

CSV = (
    "first_name,last_name,email,classroom\n"
    "Ada,Lovelace,ada@albertschool.com,MSc 1 Data\n"
    "Alan,Turing,alan@albertschool.com,MSc 1 AI\n"
)


@pytest.fixture
def roster_file(tmp_path: Path) -> Path:
    path = tmp_path / "2026-10-04.csv"
    path.write_text(CSV, encoding="utf-8")
    return path


def test_load_roster_reads_one_pair_per_row(roster_file: Path) -> None:
    pairs = load_roster(roster_file)
    assert [(s.first_name, room) for s, room in pairs] == [
        ("Ada", "MSc 1 Data"),
        ("Alan", "MSc 1 AI"),
    ]


def test_process_roster_numbers_students_in_file_order(roster_file: Path) -> None:
    registry = process_roster(roster_file)
    assert [s.student_id for s in registry] == [1, 2]


def test_cli_roster_prints_a_summary(roster_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    main(["roster", str(roster_file)])
    assert capsys.readouterr().out.splitlines()[-1] == "2 students registered"
