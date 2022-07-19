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

normal_course_list=[
    "CSC111",
    "CSC115",
    "CSC225",
    "CSC226",
    "CSC230",
    "CSC320",
    "CSC360",
    "CSC361",
    "CSC370",
    "ECE300",
    "ECE310",
    "ECE320",
    "ECE330",
    "ECE340",
    "ECE360",
    "ECE455",
    "ECE458",
    "ECE488",
    "SENG265",
    "SENG275",
    "SENG310",
    "SENG321",
    "SENG371",
    "SENG401",
    "SENG468",
    "SENG474",
    "CSC355",
    "ECE216",
    "ECE241",
    "ECE250",
    "ECE255",
    "ECE260",
    "ECE350",
    "ECE355",
    "ECE356",
    "ECE365",
    "ECE370",
    "ECE380",
    "ECE399",
    "ECE403",
    "ECE463",
    "SENG350",
    "SENG360",
    "ECE220",
    "ECE242",
    "ECE299",
    "ECE410",
    "ECE499",
    "SENG426",
    "SENG440",
    "SENG499",
    "CSC460",
    "SENG411",
    "SENG421",
    "SENG435",
    "SENG466"
]

out_of_scope_course_list=[
    "MATH122",
    "ENGR002",
    "MATH109",
    "MATH100",
    "MATH110",
    "ENGR130",
    "ENGR110",
    "PHYS110",
    "MATH101",
    "ENGR120",
    "ENGR141",
    "PHYS111",
    "ENGR001",
    "CHEM101",
    "CHEM150",
    "STAT260",
    "ECON180",
    "ENGR003",
    "ENGR004"]
sample_new_course_list = [
    "MATH129",
    "ENGR187",
    "PHYS143",
    "MATH191",
    "CSC227",
    "SENG188"
]

def load_courses(course_type: str) -> list[dict]:
    """Loads the list of courses that were used to train the model."""
    if course_type == "OOS": # out of scope course
        courses = out_of_scope_course_list
    elif course_type == "normal": # normal courses
        courses = normal_course_list
    else: # new courses:
        courses = sample_new_course_list

    return list(dict.fromkeys(courses))


class CourseProvider(BaseProvider):
    """Provides generators for courses."""
    def semester(self) -> str:
        """Generates a random semester."""
        semesters = ["FALL", "SPRING"]
        return random.choice(semesters)

    def course(self, course_type: str) -> dict:
        """Generates a random course from the list of valid courses."""
        choice = re.split(r"(\d+)", random.choice(load_courses(course_type)))
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
