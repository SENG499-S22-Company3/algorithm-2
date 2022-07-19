"""Unit Tests for HTTP Endpoints

This script uses the unittest framework to implement unit tests for the endpoints of Algorithm 2.
"""
import ast
import json
import unittest
import random
from test_base import BaseCase


class EndpointTests(BaseCase):
    """Encompasses the endpoint unit tests."""
    def test_index(self) -> None:
        """Tests that the index page returns a 200 response."""
        response = self.app.get("/")
        status = response.status_code
        self.assertEqual(status, 200)

    def test_post_response(self) -> None:
        """Tests that the predict_class_size endpoint returns a 200 response."""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course(course_type="NORMAL")
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": self.fake.semester(),
                "capacity": 0
            }
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Check response code
        self.assertEqual(response.status_code, 200)

    ####### UNIT TESTS MAIN USE CASES #######
    def test_normal_course_case1(self) -> None:
        """ Tests returned capacity for courses we must make a prediction on (ECE/SENG/CSC)
            Case 1: input capacity is > 0 so output capacity == input capacity (unchanged)"""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course(course_type="NORMAL")
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": self.fake.semester(),
                "capacity": random.randint(1, 1000)
            }
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm returns a positive capacity
        for course in response_courses:
            self.assertGreater(course["capacity"], 0)

    def test_normal_course_case2(self) -> None:
        """ Tests returned capacity for courses we must make a prediction on (ECE/SENG/CSC)
            Case 2: input capacity == 0 so output capacity > 0 (predicted)"""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course(course_type="NORMAL")
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": self.fake.semester(),
                "capacity": 0
            }
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm returns a postive capacity
        for course in response_courses:
            self.assertGreater(course["capacity"], 0)

    def test_oos_course_case1(self) -> None:
        """ Courses that are in our Program but are out of scope for our schedulator (ECON180, MATH122, etc.)
            Case 1: input capacity is >= 0 so output capacity == input capacity (unchanged)"""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course(course_type="OOS")
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": self.fake.semester(),
                "capacity": random.randint(0, 1000)
            }
            course['input_capacity'] = course['capacity']
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm does not change the input capacity
        for course in response_courses:
            self.assertEqual(course["capacity"], course['input_capacity'])

    def test_new_course_case1(self) -> None:
        """ New courses that are being offered for the first time must have default capacity of 80 (CSC227)
            Case 1: input capacity is > 0 so output capacity == input capacity (unchanged)"""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course(course_type="NEW")
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": self.fake.semester(),
                "capacity": 0,
                "capacity": random.randint(1, 1000)
            }
            course['input_capacity'] = course['capacity']
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm does not change the input capacity
        for course in response_courses:
            self.assertEqual(course["capacity"],  course['input_capacity'])

    def test_new_course_case2(self) -> None:
        """ New courses that are being offered for the first time must have default capacity of 80 (CSC227)
            Case 2: input capacity == 0 so output capacity == 80 (default assigned)"""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course(course_type="NEW")
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": self.fake.semester(),
                "capacity": 0
            }
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm assigns default 80 capacity
        for course in response_courses:
            self.assertEqual(course["capacity"], 80)


if __name__ == "__main__":
    unittest.main()
