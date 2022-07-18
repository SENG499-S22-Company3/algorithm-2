"""Unit Tests for HTTP Endpoints

This script uses the unittest framework to implement unit tests for the endpoints of Algorithm 2.
"""
import ast
import json
import unittest
from .test_base import BaseCase


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
            faked_course = self.fake.course()
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

    def test_nonnegative_capacity(self) -> None:
        """Tests that the predict_class_size endpoint does not return a negative number as a capacity."""
        # Change this number to modify the number of randomly generated courses
        number_of_test_courses = 100

        courses = []
        for _ in range(number_of_test_courses):
            faked_course = self.fake.course()
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
            print(course)
            self.assertGreater(course["capacity"], 0)


if __name__ == "__main__":
    unittest.main()
