"""JSON Data Parsing Script

This script takes raw JSON course data and parses and filters it for use in the best-fit algorithm.
"""
from argparse import ArgumentParser
from csv import DictWriter
import os
import json

RAW_COURSE_DATA_FILE = "data/course_data.json"
RAW_ENROLLMENT_DATA_FILE = "data/yearEnrollmentData.json"

course_list=[
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
    #"CSC460",
    #"SENG411",
    #"SENG421",
    #"SENG435",
    #"SENG466"
]

def load_json(json_file: str) -> list[dict]:
    """Returns JSON data in the form of a list of dictionaries given a filename string."""
    data = []
    try:
        with open(json_file, encoding="utf8") as file_:
            data = json.load(file_, strict=False)
    except FileNotFoundError:
        print("Raw data file missing. Be sure to un-zip the data in the raw_data/ folder.")
        exit(1)

    return data

def parse_json(json_file: str) -> list[dict]:
    """Returns JSON data in the form of a list of dictionaries with a filtered set of fields given
    a filename string"""
    data = load_json(json_file)

    parsed_data = []

    for course in data:
        if course:
            parsed_course = {}

            parsed_course["id"] = course["id"]
            parsed_course["term"] = course["term"]
            parsed_course["termDesc"] = course["termDesc"]
            parsed_course["courseReferenceNumber"] = course["courseReferenceNumber"]
            parsed_course["courseNumber"] = course["courseNumber"]
            parsed_course["subject"] = course["subject"]
            parsed_course["sequenceNumber"] = course["sequenceNumber"]
            parsed_course["scheduleTypeDescription"] = course["scheduleTypeDescription"]
            parsed_course["courseTitle"] = course["courseTitle"]
            parsed_course["maximumEnrollment"] = course["maximumEnrollment"]
            parsed_course["enrollment"] = course["enrollment"]
            parsed_course["waitCapacity"] = course["waitCapacity"]
            parsed_course["waitCount"] = course["waitCount"]
            parsed_course["instructionalMethod"] = course["instructionalMethod"]

            parsed_data.append(parsed_course)

    return parsed_data

def filter_data(data: list[dict]) -> list[dict]:
    """Filters a list of courses to only include SENG and CSC lectures."""
    filtered_data = []
    for course in data:
        if (course["subject"] + course["courseNumber"]) in course_list and \
           course["sequenceNumber"] in ("A01", "A02", "A03", "A04", "A05", "A06"):
            filtered_data.append(course)

    return filtered_data


def sort_by_year(data: list[dict]) -> list[dict]:
    """Sorts a list of courses by date offered."""
    keys = lambda d: (int(d["term"]), d["subject"], d["courseNumber"], d["sequenceNumber"])
    return sorted(data, key=keys)


def main() -> None:
    """Main function."""
    parser = ArgumentParser(description="Data Parser")
    parser.add_argument("-c", action="store_true", dest="csv", help="output data frame to .csv")
    parser.add_argument("-j", action="store_true", dest="json", help="output data frame to .json")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided.")

    # Setup input and output file paths
    script_dir = os.path.dirname(__file__)
    abs_in_file_path = os.path.join(script_dir, RAW_COURSE_DATA_FILE)
    output_dir = os.path.join(script_dir, "data\\")

    # Parse and filter the data
    data = sort_by_year(filter_data(parse_json(abs_in_file_path)))

    # Create an output folder if one is missing
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if args.json:
        abs_out_file_path = os.path.join(output_dir, "output.json")

        with open(abs_out_file_path, "w", encoding="utf-8") as file_:
            json.dump(data, file_, ensure_ascii=False, indent=4)

    if args.csv:
        abs_out_file_path = os.path.join(output_dir, args.csv)

        with open(abs_out_file_path, "w", encoding="utf-8", newline='') as file_:
            keys = data[0].keys()
            dict_writer = DictWriter(file_, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

if __name__ == "__main__":
    main()
