import csv
from pathlib import Path

from greetings.student import Student


def load_roster(path: Path) -> list[tuple[Student, str]]:
    """Read a roster CSV: one (student, classroom) pair per row."""
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            (Student(row["first_name"], row["last_name"], row["email"]), row["classroom"])
            for row in csv.DictReader(handle)
        ]


def process_roster(path: Path) -> list[Student]:
    """Welcome, register and enroll every student of a roster file."""
    registry: list[Student] = []
    for student, classroom in load_roster(path):
        student.register(registry)
        print(student.welcome())
        print(student.enroll(classroom))
    print(f"{len(registry)} students registered")
    return registry
