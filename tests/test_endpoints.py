"""Unit Tests for HTTP Endpoints

This script uses the unittest framework to implement unit tests for the endpoints of Algorithm 2.
"""
import ast
import json
import unittest
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

    def test_normal_course(self) -> None:
        """ Tests returned capacity for courses we must make a prediction on (ECE/SENG/CSC)
            Case 1: input capacity is > 0 so output capacity == input capacity (unchanged)
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

        # Check that the algorithm does not return a negative capacity
        for course in response_courses:
            self.assertGreater(course["capacity"], 0)

    def test_oos_course(self) -> None:
        """ Tests returned capacity for courses we must make a prediction on (ECE/SENG/CSC)
            Case 1: input capacity is > 0 so output capacity == input capacity (unchanged)
            Case 2: input capacity == 0 so output capacity > 0 (predicted)"""
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
                "capacity": 0
            }
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm does not return a negative capacity
        for course in response_courses:
            self.assertEqual(course["capacity"], 0)


    def test_new_course(self) -> None:
        """ Tests returned capacity for courses we must make a prediction on (ECE/SENG/CSC)
            Case 1: input capacity is > 0 so output capacity == input capacity (unchanged)
            Case 2: input capacity == 0 so output capacity > 0 (predicted)"""
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

        # Check that the algorithm does not return a negative capacity
        for course in response_courses:
            self.assertEqual(course["capacity"], 80)

    def test_duplicate_courses(self) -> None:
        """ Tests returned capacity for duplicate courses we must make a prediction on (ECE/SENG/CSC)
            Case: Duplicate courses in the same semester should all output the same capacity"""
        # Change this number to modify the number of generated courses
        number_of_test_courses = 100

        courses = []
        faked_course = self.fake.course(course_type="NORMAL")
        semester=self.fake.semester()

        for _ in range(number_of_test_courses):
            course = {
                "subject": faked_course["subject"],
                "code": faked_course["code"],
                "seng_ratio": self.fake.pyfloat(left_digits=1,
                                                right_digits=2,
                                                max_value=1,
                                                positive=True),
                "semester": semester,
                "capacity": 0
            }
            courses.append(course)

        payload = json.dumps(courses)
        response = self.app.post("/predict_class_size",
                                 data=payload,
                                 content_type="application/json")

        # Convert response data to Python object
        response_courses = ast.literal_eval(response.data.decode("UTF-8"))

        # Check that the algorithm returns the same capacity for duplicate courses
        for course in response_courses:
            self.assertEqual(response_courses[0]["capacity"], course["capacity"])


if __name__ == "__main__":
    unittest.main()
