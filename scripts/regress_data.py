import os
import json
import pandas
from sklearn import linear_model
from collections import defaultdict

pandas.options.mode.chained_assignment = None

PARSE_OUTPUT_PATH = "/output/output2.json"
ENROLLMENT_DATA_PATH = "/output/yearEnrollmentData.json"

course_list_to_predict = {
	"MATH122": [],
	"ENGR002": ["MATH122"],
	"CSC111": [],
	"CSC115": ["CSC111"],
	"CSC230": ["CSC111", "CSC115"],
	"ECE255": ["CSC111", "CSC115"],
	"CSC225": ["CSC115", "MATH122"],
	"SENG265": ["CSC115"],
	"SENG310": ["SENG265"],
	"SENG360": ["CSC230", "ECE255","SENG265","CSC226"],
	"CSC360": ["SENG265"],
	"CSC226": ["CSC225"],
	"SENG321": ["SENG265"],
	"SENG275": ["SENG265"],
	"CSC355": ["CSC230", "ECE255", "MATH122"],
	"ECE355": ["CSC230", "ECE255"],
	"CSC320": ["CSC226"],
	"CSC370": ["SENG265","CSC226"],
	"SENG371": ["SENG275"],
	"SENG440": ["CSC355", "ECE355"],
	"CSC361": ["CSC230", "ECE255","SENG265","CSC226"],
	"ECE458": ["CSC230", "ECE255","SENG265","CSC226"],
	"SENG426": ["SENG275","SENG371"],
	"SENG350": ["SENG275"],
	"CSC460": ["CSC360","CSC355", "ECE355"],
	"ECE455": ["CSC360","CSC355", "ECE355"],
	"SENG499": ["SENG321","CSC370","CSC361", "ECE458","SENG350"],
	"SENG401": []
}

def load_json(json_file: str) -> list[dict]:
		"""Returns JSON data in the form of a list of dictionaries given a filename string."""
		
		data = []
		with open(json_file, encoding="utf8") as file_:
			data = json.load(file_, strict=False)
		return data

def parse_enrollment_data(enrollment_json_data):
	
	parsed_data = defaultdict(list)
	for year in enrollment_json_data:
		parsed_data[year['year']].append( [year['year'],  year['1stYear'],  year['2ndYear'] + year['2ndYearTransfer'],  year['3rdYear'],  year['4thYear'] + year['5thYear'] + year['6thYear'] + year['7thYear']])
	return parsed_data

def check_if_course_exists(course_list, course_term):
	
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
			list_index = check_if_course_exists(course_dictionary[course_name], course_term)
			if list_index > -1:
				course_dictionary[course_name][list_index]['class_size'] = course_dictionary[course_name][list_index]['class_size'] + course['enrollment']
			else:
				course_dictionary[course_name].append({'course_name': course_name, 'term': int(course['term']), 'class_size': course['enrollment']})
		else:
			course_dictionary[course_name].append({'course_name': course_name, 'term': int(course['term']), 'class_size': course['enrollment']})
	
	print(f'unique keys count: {len(course_dictionary.keys())}')
	return course_dictionary

def create_regress_models():
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
			
			for i in range(0,len(X_values)):
				print(X_values[i], Y_values[i])

			temp_regr_model = linear_model.LinearRegression()
			temp_regr_model.fit(X_values, Y_values)
			regr_models.update({course: temp_regr_model})
	return regr_models

def main():


	course_regr_models = create_regress_models()
	print(course_regr_models)
	

if __name__ == "__main__":
		main()
