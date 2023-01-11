from datetime import datetime

from topper_student import get_topper_student


def test_student_get_age(dummy_student):
    dummy_student_age = (datetime.now() - dummy_student.dob).days // 365
    assert dummy_student.get_age() == dummy_student_age


def test_student_get_credits(dummy_student):
    assert dummy_student.get_credits() == 20


def test_get_topper(make_dummy_students):
    students = [
        make_dummy_students("rakesh", 20),
        make_dummy_students("bavuma", 19),
        make_dummy_students("Tukaram", 17)
    ]

    topper = get_topper_student(students)
    assert topper == students[0]