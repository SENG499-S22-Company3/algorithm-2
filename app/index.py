from lib2to3.pgen2.pgen import DFAState
from flask import Flask, jsonify, request
from marshmallow import EXCLUDE

from app.models.course import Course, CourseSchema, Semester
from app.data.course_path import course_list
from app.featureEngineer.featureEngineer import pre_process
from app.models.model import model_predict


app = Flask(__name__)

@app.route('/')
def get_all_courses():
  schema = CourseSchema(many=True)
  seng_courses = schema.dump(
    course_list
  )
  return jsonify(seng_courses)


@app.route('/seng')
def get_seng_courses():
  schema = CourseSchema(many=True)
  seng_courses = schema.dump(
    filter(lambda t: t.department == "Software Engineering" or t.department == "Computer Science", course_list)
  )
  return jsonify(seng_courses)


@app.route('/', methods=['POST'])
def add_course():
  course = CourseSchema().load(request.get_json(), unknown=EXCLUDE)
  course_list.append(course)
  return "", 204


@app.route('/predict_class_size', methods=['POST'])
def predict():
  data = request.get_json()
  df = pre_process(data)
  capacity = model_predict(data,df)
  return capacity




