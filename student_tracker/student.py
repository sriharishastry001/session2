"""
Student class module.
"""

from typing import Dict, Any, Optional


class Student:
    """
    Represents an individual student with ID, name, and grades for subjects.
    """

    def __init__(self, student_id: str, name: str, grades: Optional[Dict[str, float]] = None):
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise ValueError("Student name must be a non-empty string.")

        self.student_id = student_id.strip()
        self.name = name.strip()
        self.grades: Dict[str, float] = {}

        if grades:
            for subject, grade in grades.items():
                self.add_grade(subject, grade)

    def add_grade(self, subject: str, grade: float) -> None:
        """Add or update a grade for a subject (0 to 100)."""
        if not subject or not isinstance(subject, str):
            raise ValueError("Subject must be a non-empty string.")

        try:
            grade_val = float(grade)
        except (ValueError, TypeError):
            raise ValueError("Grade must be a numeric value.")

        if not (0.0 <= grade_val <= 100.0):
            raise ValueError("Grade must be between 0 and 100.")

        self.grades[subject.strip()] = grade_val

    def remove_grade(self, subject: str) -> bool:
        """Remove grade for a subject. Returns True if removed, False if not found."""
        subject_clean = subject.strip()
        if subject_clean in self.grades:
            del self.grades[subject_clean]
            return True
        return False

    def calculate_average(self) -> float:
        """Calculate average grade across all subjects."""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def get_letter_grade(self) -> str:
        """Return letter grade based on calculated average."""
        avg = self.calculate_average()
        if not self.grades:
            return "N/A"
        if avg >= 90.0:
            return "A"
        elif avg >= 80.0:
            return "B"
        elif avg >= 70.0:
            return "C"
        elif avg >= 60.0:
            return "D"
        else:
            return "F"

    def to_dict(self) -> Dict[str, Any]:
        """Convert Student object to a dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades.copy(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Create a Student object from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            grades=data.get("grades", {}),
        )

    def __str__(self) -> str:
        avg = self.calculate_average()
        letter = self.get_letter_grade()
        return f"Student[ID={self.student_id}, Name='{self.name}', Average={avg:.2f} ({letter})]"

    def __repr__(self) -> str:
        return f"Student(student_id={self.student_id!r}, name={self.name!r}, grades={self.grades!r})"
