import os
import json
import pandas
from sklearn import linear_model
from collections import defaultdict
import sys, os

PATH = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(PATH)

from app.enrollment_prediction import predict_enrollment

pandas.options.mode.chained_assignment = None

PARSE_OUTPUT_PATH = "/output/output2.json"
ENROLLMENT_DATA_PATH = "/output/yearEnrollmentData.json"

course_list_to_predict = {
	"MATH122",
	"ENGR002",
	"CSC111",
	"CSC115",
	"CSC230",
	"ECE255",
	"CSC225",
	"SENG265",
	"SENG310",
	"SENG360",
	"CSC360",
	"CSC226",
	"SENG321",
	"SENG275",
	"CSC355",
	"ECE355",
	"CSC320",
	"CSC370",
	"SENG371",
	"SENG440",
	"CSC361",
	"ECE458",
	"SENG426",
	"SENG350",
	"CSC460",
	"ECE455",
	"SENG499",
	"SENG401"
}

def load_json(json_file: str) -> list[dict]:
		"""Returns JSON data in the form of a list of dictionaries given a filename string."""
		
		data = []
		with open(json_file, encoding="utf8") as file_:
			data = json.load(file_, strict=False)
		return data

def parse_enrollment_data(enrollment_json_data):
	"""Returns a dictionary with data filtered out"""
	
	parsed_data = defaultdict(list)
	for year in enrollment_json_data:
		parsed_data[year['year']].append( [year['year'],  year['1stYear'],  year['2ndYear'] + year['2ndYearTransfer'],  year['3rdYear'],  year['4thYear'] + year['5thYear'] + year['6thYear'] + year['7thYear']])
	return parsed_data

def get_course_section_index(course_list, course_term):
	"""Checks if a course in a specific term already exists in the list. Used to add up all different course sections"""
	
	for index in range (0, len(course_list)):
		if course_list[index]['term'] == course_term:
			return index
	return -1

def create_course_dictionary(course_json_file: str):
	"""Returns a dictionary
		Key: Course name (for example: CSC111)
		Value: List of courses  name as the key and a list of all the times it was taught"""

	course_json_data = load_json(course_json_file)
	course_dictionary = defaultdict(list)
	
	for course in course_json_data:
		course_name = course['subject'] + course['courseNumber']
		course_term = int(course['term'])

		if course_name in course_dictionary.keys():
			list_index = get_course_section_index(course_dictionary[course_name], course_term)
			if list_index > -1:
				course_dictionary[course_name][list_index]['class_size'] = course_dictionary[course_name][list_index]['class_size'] + course['enrollment']
			else:
				course_dictionary[course_name].append({'course_name': course_name, 'term': int(course['term']), 'class_size': course['enrollment']})
		else:
			course_dictionary[course_name].append({'course_name': course_name, 'term': int(course['term']), 'class_size': course['enrollment']})
	
	# print(f'unique keys count: {len(course_dictionary.keys())}')
	return course_dictionary

def create_regress_models():
	"""Creates a multiple-linear regresion model for each course and trains it based on previous data
		Output: Dictionary with the course as the key and the regress model as the value
	"""
	
	course_dictionary = create_course_dictionary(os.path.dirname(__file__) + PARSE_OUTPUT_PATH)
	enrollment_json_data = load_json(os.path.dirname(__file__) + ENROLLMENT_DATA_PATH)
	enrollment_dictionary = parse_enrollment_data(enrollment_json_data)
	
	course_list = []
	for key in course_dictionary.keys():
		for element in course_dictionary[key]:
			course_list.append([element['course_name'], element['term'], element['class_size']])

	df = pandas.DataFrame(course_list, columns =['course_name', 'term', 'class_size'])
	df = df.pivot(index = 'term', columns = 'course_name', values = 'class_size').fillna(0).astype(int)
	df['semester'] = (df.index%100/4).astype(int)
	df.index = (df.index/100).astype(int)
	
	regr_models = {}
	
	for course in course_list_to_predict:
		
		if course in df.columns:
			# course_df = pandas.DataFrame(columns =[course, 'term', 'class_size'])
			temp_df = df[(df[course] != 0) & (df.index < 2022) & (df.index > 2013)]
			temp_df['year_enrollment'] = (temp_df.index*0).astype(int)
			for index in temp_df.index:
				if index in enrollment_dictionary:
					temp_df.loc[index, 'year_enrollment'] = enrollment_dictionary[index][0][int(course[-3])]
			
			X_values = temp_df[['semester', 'year_enrollment']].values
			Y_values = temp_df[[course]].values
			
			temp_regr_model = linear_model.LinearRegression()
			temp_regr_model.fit(X_values, Y_values)
			regr_models.update({course: temp_regr_model})
	return regr_models

def predict_enrollment_year(regr_model_dictionary, semester, year_to_predict):
	""""
	This function takes in the trained regress models and outputs the predicted results
	Input:
	- regr_model_dictionary: dictionary with regress models
	- semester: single integer specifying the semester to predict for (0 = fall, 1 = spring, 2 = summer)
	- year_to_predict: single integer specifying the year for which to predict (2022)
	"""

	year_list = [(key, value) for key, value in predict_enrollment.predict_all_years([year_to_predict])[0].items()]
	output_list = []
	
	for course in course_list_to_predict:
		if course in regr_model_dictionary:
			course_year = int(course[-3])
			predicted_size = regr_model_dictionary[course].predict([[semester, year_list[course_year][1]]])[0][0]
			predicted_size = int(predicted_size*100)/100
			output_list.append((course, predicted_size))

	return output_list

def main():

	course_regr_models = create_regress_models()
	predicted_list = predict_enrollment_year(course_regr_models, 0, 2022)
	for element in predicted_list:
		print(element)
	

if __name__ == "__main__":
		main()
