from typing import Any, Mapping
from enum import Enum
from marshmallow import Schema, fields, post_load, ValidationError


class Semester(Enum):
    FALL   = 0
    SPRING = 1
    SUMMER = 2


class Course:
    def __init__(self, name: str, department: str=None, class_size: int=0,
                 semester: Semester=None, year: int=None, prereqs: list=None,
                 coreqs: list=None, required_year: int=None) -> None:
        """Initializes a course"""
        self.name = name
        self.department = department
        self.class_size = class_size
        self.semester = semester
        self.year = year
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.required_year = required_year

    def __str__(self) -> str:
        """Readable string representation"""
        if self.semester is not None and self.year is not None:
            return f"{self.name} - {self.semester.name.capitalize} {self.year}"
        return f"{self.name}"

    def __repr__(self) -> str:
        """Object representation"""
        return f"Course({self.name}, {self.department}, {self.class_size}, \
                 {self.semester}, {self.year}, {self.prereqs}, {self.coreqs}, \
                 {self.required_year})"

    def __eq__(self, other):
        """Compare courses"""
        if not isinstance(other, Course):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name


class CourseField(fields.Field):
    """Field that serializes to a string representation of a course and
    deserializes to a Course object
    """
    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value: Any, attr: str,
                     data: Mapping[str, Any], **kwargs):
        try:
            return Course(value)
        except ValueError as error:
            raise ValidationError("You dun messed up.") from error


class CourseSchema(Schema):
    name = fields.Str()
    department = fields.Str()
    class_size = fields.Integer()
    semester = fields.Integer()
    year = fields.Integer()
    prereqs = fields.List(fields.List(CourseField()))

    @post_load
    def create_course(self, data, **kwargs):
        return Course(**data)
