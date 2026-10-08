import pytest

from greetings import Student, main


def make_student() -> Student:
    return Student("Ada", "Lovelace", "ada@albertschool.com")


def test_welcome_uses_first_name() -> None:
    assert make_student().welcome() == "Welcome to Albert School, Ada!"


def test_register_returns_and_stores_the_id() -> None:
    registry: list[Student] = []
    student = make_student()
    assert student.register(registry) == 1
    assert student.student_id == 1
    assert registry == [student]


@pytest.mark.parametrize("already_registered", [0, 1, 5])
def test_register_numbers_after_the_registry_size(already_registered: int) -> None:
    registry = [make_student() for _ in range(already_registered)]
    assert make_student().register(registry) == already_registered + 1


def test_enroll_sets_the_classroom() -> None:
    student = make_student()
    assert student.enroll("MSc 1 Data") == "Ada Lovelace joins MSc 1 Data."
    assert student.classroom == "MSc 1 Data"


def test_main_prints_the_four_lines(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Welcome to Albert School, Tuka!"
    assert len(lines) == 4
