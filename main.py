#!/usr/bin/env python3
"""
Command-Line Interface (CLI) for Student Tracker.
"""

import sys
from student_tracker import Student, StudentTracker


def display_menu():
    print("\n=================================")
    print("      STUDENT TRACKER CLI        ")
    print("=================================")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. View Student Details")
    print("4. List All Students")
    print("5. Search Students")
    print("6. Add/Update Grade for Student")
    print("7. Remove Grade from Student")
    print("8. View Class Statistics")
    print("9. Save Data to File")
    print("10. Load Data from File")
    print("0. Exit")
    print("=================================")


def add_student_flow(tracker: StudentTracker):
    print("\n--- Add Student ---")
    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return
    if tracker.get_student(student_id):
        print(f"Error: Student with ID '{student_id}' already exists.")
        return

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Error: Student name cannot be empty.")
        return

    try:
        student = Student(student_id, name)
        tracker.add_student(student)
        print(f"Success: Student '{name}' (ID: {student_id}) added successfully.")
    except Exception as e:
        print(f"Error adding student: {e}")


def remove_student_flow(tracker: StudentTracker):
    print("\n--- Remove Student ---")
    student_id = input("Enter Student ID to remove: ").strip()
    if tracker.remove_student(student_id):
        print(f"Success: Student ID '{student_id}' removed.")
    else:
        print(f"Error: Student ID '{student_id}' not found.")


def view_student_flow(tracker: StudentTracker):
    print("\n--- View Student Details ---")
    student_id = input("Enter Student ID: ").strip()
    student = tracker.get_student(student_id)
    if not student:
        print(f"Error: Student ID '{student_id}' not found.")
        return

    print(f"\nID: {student.student_id}")
    print(f"Name: {student.name}")
    print(f"Average Grade: {student.calculate_average():.2f}")
    print(f"Letter Grade: {student.get_letter_grade()}")
    print("Grades:")
    if student.grades:
        for subject, grade in student.grades.items():
            print(f"  - {subject}: {grade:.2f}")
    else:
        print("  No grades recorded.")


def list_students_flow(tracker: StudentTracker):
    print("\n--- All Students ---")
    students = tracker.list_students()
    if not students:
        print("No students currently registered.")
        return

    print(f"{'ID':<10} {'Name':<25} {'Average':<10} {'Letter':<8}")
    print("-" * 55)
    for s in students:
        avg = s.calculate_average()
        letter = s.get_letter_grade()
        print(f"{s.student_id:<10} {s.name:<25} {avg:<10.2f} {letter:<8}")


def search_students_flow(tracker: StudentTracker):
    print("\n--- Search Students ---")
    query = input("Enter search query (ID or Name): ").strip()
    results = tracker.search_students(query)
    if not results:
        print("No students found matching your search.")
        return

    print(f"Found {len(results)} matching student(s):")
    print(f"{'ID':<10} {'Name':<25} {'Average':<10} {'Letter':<8}")
    print("-" * 55)
    for s in results:
        avg = s.calculate_average()
        letter = s.get_letter_grade()
        print(f"{s.student_id:<10} {s.name:<25} {avg:<10.2f} {letter:<8}")


def add_grade_flow(tracker: StudentTracker):
    print("\n--- Add/Update Grade ---")
    student_id = input("Enter Student ID: ").strip()
    student = tracker.get_student(student_id)
    if not student:
        print(f"Error: Student ID '{student_id}' not found.")
        return

    subject = input("Enter Subject Name: ").strip()
    if not subject:
        print("Error: Subject name cannot be empty.")
        return

    grade_str = input("Enter Grade (0-100): ").strip()
    try:
        grade = float(grade_str)
        student.add_grade(subject, grade)
        print(f"Success: Set grade {grade:.2f} for subject '{subject}' on student {student.name}.")
    except ValueError as e:
        print(f"Error: Invalid grade value. {e}")


def remove_grade_flow(tracker: StudentTracker):
    print("\n--- Remove Grade ---")
    student_id = input("Enter Student ID: ").strip()
    student = tracker.get_student(student_id)
    if not student:
        print(f"Error: Student ID '{student_id}' not found.")
        return

    subject = input("Enter Subject Name to remove: ").strip()
    if student.remove_grade(subject):
        print(f"Success: Grade for '{subject}' removed from {student.name}.")
    else:
        print(f"Error: Subject '{subject}' not found for {student.name}.")


def view_class_stats_flow(tracker: StudentTracker):
    print("\n--- Class Statistics ---")
    students = tracker.list_students()
    if not students:
        print("No students registered to calculate statistics.")
        return

    print(f"Total Students: {len(students)}")
    print(f"Overall Class Average: {tracker.get_class_average():.2f}")

    top_performers = tracker.get_top_performers(1)
    if top_performers:
        top = top_performers[0]
        print(f"Top Performer: {top.name} (ID: {top.student_id}) - Avg: {top.calculate_average():.2f}")

    lowest_performers = tracker.get_lowest_performers(1)
    if lowest_performers:
        low = lowest_performers[0]
        print(f"Lowest Performer: {low.name} (ID: {low.student_id}) - Avg: {low.calculate_average():.2f}")


def save_data_flow(tracker: StudentTracker):
    print("\n--- Save Data ---")
    filepath = input("Enter file path to save JSON (default: students.json): ").strip()
    if not filepath:
        filepath = "students.json"

    try:
        tracker.save_to_file(filepath)
        print(f"Success: Data successfully saved to '{filepath}'.")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data_flow(tracker: StudentTracker):
    print("\n--- Load Data ---")
    filepath = input("Enter file path to load JSON (default: students.json): ").strip()
    if not filepath:
        filepath = "students.json"

    try:
        tracker.load_from_file(filepath)
        print(f"Success: Data successfully loaded from '{filepath}'. Total students: {len(tracker.students)}.")
    except Exception as e:
        print(f"Error loading data: {e}")


def main():
    tracker = StudentTracker()
    print("Welcome to Student Tracker!")

    while True:
        display_menu()
        choice = input("Select an option (0-10): ").strip()

        if choice == "1":
            add_student_flow(tracker)
        elif choice == "2":
            remove_student_flow(tracker)
        elif choice == "3":
            view_student_flow(tracker)
        elif choice == "4":
            list_students_flow(tracker)
        elif choice == "5":
            search_students_flow(tracker)
        elif choice == "6":
            add_grade_flow(tracker)
        elif choice == "7":
            remove_grade_flow(tracker)
        elif choice == "8":
            view_class_stats_flow(tracker)
        elif choice == "9":
            save_data_flow(tracker)
        elif choice == "10":
            load_data_flow(tracker)
        elif choice == "0":
            print("Exiting Student Tracker. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Please enter a number between 0 and 10.")


if __name__ == "__main__":
    main()
