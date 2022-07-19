from marshmallow import EXCLUDE
from flask import Flask, jsonify, request
from app.models.course import CourseSchema
from app.models.model import model_predict
from app.data.course_path import course_list
from app.featureEngineer.featureEngineer import pre_process


app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
  return "OK"


@app.route("/")
def get_all_courses():
  schema = CourseSchema(many=True)
  seng_courses = schema.dump(
    course_list
  )
  return jsonify(seng_courses)


@app.route("/seng")
def get_seng_courses():
  schema = CourseSchema(many=True)
  seng_courses = schema.dump(
    filter(lambda t: t.department == "Software Engineering" or t.department == "Computer Science", course_list)
  )
  return jsonify(seng_courses)


@app.route("/", methods=["POST"])
def add_course():
  course = CourseSchema().load(request.get_json(), unknown=EXCLUDE)
  course_list.append(course)
  return "", 204


@app.route("/predict_class_size", methods=["POST"])
def predict():
  data = request.get_json()
  df = pre_process(data)
  capacity = model_predict(data, df)
  return jsonify(capacity)
