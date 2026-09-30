"""
StudentTracker class module.
"""

import json
import os
from typing import Dict, List, Optional, Any
from .student import Student


class StudentTracker:
    """
    Manages a collection of students and provides search, statistical,
    and persistence capabilities.
    """

    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, student: Student) -> bool:
        """Add a student to the tracker. Returns False if student_id already exists."""
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by student_id. Returns True if removed, False otherwise."""
        student_id_clean = student_id.strip()
        if student_id_clean in self.students:
            del self.students[student_id_clean]
            return True
        return False

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve a student by student_id."""
        return self.students.get(student_id.strip())

    def list_students(self) -> List[Student]:
        """List all students sorted by student_id."""
        return sorted(self.students.values(), key=lambda s: s.student_id)

    def search_students(self, query: str) -> List[Student]:
        """
        Search for students matching query in student_id or name (case-insensitive).
        """
        q = query.strip().lower()
        if not q:
            return []
        return [
            s for s in self.students.values()
            if q in s.student_id.lower() or q in s.name.lower()
        ]

    def get_class_average(self) -> float:
        """Calculate the average grade across all students in all subjects."""
        if not self.students:
            return 0.0

        all_grades = []
        for student in self.students.values():
            all_grades.extend(student.grades.values())

        if not all_grades:
            return 0.0

        return sum(all_grades) / len(all_grades)

    def get_top_performers(self, n: int = 1) -> List[Student]:
        """Return top N students with highest average grade."""
        if not self.students or n <= 0:
            return []
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.calculate_average(),
            reverse=True
        )
        return sorted_students[:n]

    def get_lowest_performers(self, n: int = 1) -> List[Student]:
        """Return lowest N students with lowest average grade."""
        if not self.students or n <= 0:
            return []
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.calculate_average()
        )
        return sorted_students[:n]

    def save_to_file(self, filepath: str) -> None:
        """Save student tracker state to a JSON file."""
        data = {
            "students": [student.to_dict() for student in self.students.values()]
        }
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filepath: str) -> None:
        """Load student tracker state from a JSON file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.students.clear()
        for student_data in data.get("students", []):
            student = Student.from_dict(student_data)
            self.add_student(student)
