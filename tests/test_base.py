"""Unit Test Base

This module sets up the base test case for Algorithm 2 unit tests.
"""
import os
import re
import sys
import json
import random
import unittest
from faker import Faker
from faker.providers import BaseProvider

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from app.index import app


def load_courses() -> list[dict]:
    """Loads the list of courses that were used to train the model."""
    with open("app/models/data/training_data.json", "rb") as json_file:
        data = json.load(json_file)
    courses = []
    for key in data["subjectCourse"].values():
        courses.append(key)
    return list(dict.fromkeys(courses))


class CourseProvider(BaseProvider):
    """Provides generators for courses."""
    def semester(self) -> str:
        """Generates a random semester."""
        semesters = ["FALL", "SPRING"]
        return random.choice(semesters)

    def course(self) -> dict:
        """Generates a random course from the list of valid courses."""
        choice = re.split(r"(\d+)", random.choice(load_courses()))
        course = {
            "subject": choice[0],
            "code": choice[1]
        }
        return course


class BaseCase(unittest.TestCase):
    """Base class for unit tests."""
    def setUp(self) -> None:
        self.app = app.test_client()
        self.fake = Faker()
        self.fake.add_provider(CourseProvider)
