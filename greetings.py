class Student:
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id: int | None = None
        self.classroom: str | None = None

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def welcome(self) -> str:
        return f"Welcome to Albert School Paris, {self.first_name}! Your desk is ready."

    def register(self, registry: list["Student"]) -> int:
        self.student_id = len(registry)
        registry.append(self)
        return self.student_id

    def is_enrolled(self) -> bool:
        return self.classroom is not None

    def enroll(self, classroom: str) -> str:
        self.classroom = classroom
        return f"{self.full_name()} joins {classroom}."

    def farewell(self) -> str:
        return f"See you soon, {self.first_name}!"


def main() -> None:
    registry: list[Student] = []
    student = Student("Tuka", "Bade", "tuka@albertschool.com")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id} of {len(registry)}")
    print(f"Confirmation sent to {student.email}")
    print(student.enroll("MSc 1 Data"))
    print(student.farewell())


if __name__ == "__main__":
    main()
