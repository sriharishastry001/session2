"""
Unit tests for Student and StudentTracker classes.
"""

import os
import tempfile
import pytest
from student_tracker import Student, StudentTracker


class TestStudent:
    def test_student_initialization_and_validation(self):
        s = Student("101", "Alice")
        assert s.student_id == "101"
        assert s.name == "Alice"
        assert s.grades == {}

        with pytest.raises(ValueError):
            Student("", "Alice")
        with pytest.raises(ValueError):
            Student("101", "")

    def test_add_and_remove_grades(self):
        s = Student("101", "Alice")
        s.add_grade("Math", 95)
        s.add_grade("Science", 85)
        assert s.grades == {"Math": 95.0, "Science": 85.0}

        # Invalid grade values
        with pytest.raises(ValueError):
            s.add_grade("History", 105)
        with pytest.raises(ValueError):
            s.add_grade("History", -5)
        with pytest.raises(ValueError):
            s.add_grade("History", "invalid")

        # Remove grade
        assert s.remove_grade("Math") is True
        assert "Math" not in s.grades
        assert s.remove_grade("NonExistent") is False

    def test_average_and_letter_grade(self):
        s = Student("101", "Alice")
        assert s.calculate_average() == 0.0
        assert s.get_letter_grade() == "N/A"

        s.add_grade("Math", 90)
        s.add_grade("Science", 80)
        assert s.calculate_average() == 85.0
        assert s.get_letter_grade() == "B"

        s.add_grade("English", 100)
        assert s.calculate_average() == 90.0
        assert s.get_letter_grade() == "A"

    def test_dict_serialization(self):
        s = Student("101", "Alice", {"Math": 90.0, "Physics": 80.0})
        data = s.to_dict()
        assert data == {
            "student_id": "101",
            "name": "Alice",
            "grades": {"Math": 90.0, "Physics": 80.0}
        }

        restored = Student.from_dict(data)
        assert restored.student_id == s.student_id
        assert restored.name == s.name
        assert restored.grades == s.grades


class TestStudentTracker:
    def test_add_get_remove_student(self):
        tracker = StudentTracker()
        s1 = Student("101", "Alice")
        s2 = Student("102", "Bob")

        assert tracker.add_student(s1) is True
        assert tracker.add_student(s1) is False  # Duplicate ID
        assert tracker.add_student(s2) is True

        assert tracker.get_student("101") == s1
        assert tracker.get_student("999") is None

        students = tracker.list_students()
        assert len(students) == 2
        assert students[0].student_id == "101"
        assert students[1].student_id == "102"

        assert tracker.remove_student("101") is True
        assert tracker.get_student("101") is None
        assert tracker.remove_student("101") is False

    def test_search_students(self):
        tracker = StudentTracker()
        tracker.add_student(Student("101", "Alice Smith"))
        tracker.add_student(Student("102", "Bob Johnson"))
        tracker.add_student(Student("201", "Charlie Brown"))

        results = tracker.search_students("alice")
        assert len(results) == 1
        assert results[0].name == "Alice Smith"

        results_id = tracker.search_students("201")
        assert len(results_id) == 1
        assert results_id[0].name == "Charlie Brown"

        assert tracker.search_students("nonexistent") == []

    def test_class_statistics(self):
        tracker = StudentTracker()
        assert tracker.get_class_average() == 0.0
        assert tracker.get_top_performers(1) == []
        assert tracker.get_lowest_performers(1) == []

        s1 = Student("101", "Alice", {"Math": 90, "Science": 100})  # Avg 95
        s2 = Student("102", "Bob", {"Math": 70, "Science": 80})    # Avg 75
        s3 = Student("103", "Charlie", {"Math": 50, "Science": 60}) # Avg 55

        tracker.add_student(s1)
        tracker.add_student(s2)
        tracker.add_student(s3)

        assert pytest.approx(tracker.get_class_average(), 0.01) == 75.0

        top = tracker.get_top_performers(1)
        assert len(top) == 1
        assert top[0].name == "Alice"

        lowest = tracker.get_lowest_performers(1)
        assert len(lowest) == 1
        assert lowest[0].name == "Charlie"

    def test_json_persistence(self):
        tracker = StudentTracker()
        s1 = Student("101", "Alice", {"Math": 95})
        s2 = Student("102", "Bob", {"Science": 88})
        tracker.add_student(s1)
        tracker.add_student(s2)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            tracker.save_to_file(tmp_path)

            new_tracker = StudentTracker()
            new_tracker.load_from_file(tmp_path)

            assert len(new_tracker.students) == 2
            loaded_s1 = new_tracker.get_student("101")
            assert loaded_s1 is not None
            assert loaded_s1.name == "Alice"
            assert loaded_s1.grades == {"Math": 95.0}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
