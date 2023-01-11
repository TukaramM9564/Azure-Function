from datetime import datetime

import pytest

from topper_student import Student


@pytest.fixture
def dummy_student():
    return Student("Tukaram", datetime(1999,2,15), "MECH", 20)


@pytest.fixture
def make_dummy_students():
    def _make_dummy_student(name, credits):
        return Student(name, datetime(1998, 2, 15), "MECH", credits)

    return _make_dummy_student