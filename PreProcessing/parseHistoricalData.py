import json

processedData = []

# List
classlist = [
    "CSC111",
    "CSC115",
    "CSC225",
    "CSC226",
    "CSC230",
    "CSC320",
    "CSC355",
    "CSC360",
    "CSC361",
    "CSC370",
    "CSC460",
    "ECE216",
    "ECE220",
    "ECE241",
    "ECE242",
    "ECE250",
    "ECE255",
    "ECE260",
    "ECE299",
    "ECE300",
    "ECE310",
    "ECE320",
    "ECE330",
    "ECE340",
    "ECE350",
    "ECE355",
    "ECE356",
    "ECE360",
    "ECE365",
    "ECE370",
    "ECE380",
    "ECE399",
    "ECE403",
    "ECE410",
    "ECE455",
    "ECE458",
    "ECE463",
    "ECE488",
    "ECE499",
    "ENG371",
    "SENG265",
    "SENG275",
    "SENG310",
    "SENG321",
    "SENG350",
    "SENG360",
    "SENG371",
    "SENG401",
    "SENG411",
    "SENG421",
    "SENG426",
    "SENG435",
    "SENG440",
    "SENG466",
    "SENG468",
    "SENG474",
    "SENG499"
]

print("Reading input data")
with open("data/banner.json", encoding="utf8") as jsonfile:
    histClassData = json.load(jsonfile)

print("Starting Processing ...")
for elem in histClassData:
    if elem:
        # Replace ELEC and CENG with ECE
        if  elem["subject"] in ["ELEC", "CENG"]:
            elem["subjectCourse"] = elem["subjectCourse"].replace("CENG", "ECE")
            elem["subjectCourse"] = elem["subjectCourse"].replace("ELEC", "ECE")

        # Filter out courses not in the classlist
        if elem["subjectCourse"] in classlist:
            if "B" not in elem["sequenceNumber"] and "T" not in elem["sequenceNumber"]:
                if not any(e["id"] == elem["id"] for e in processedData):
                    dic = {
                        "id": elem["id"],
                        "term": elem["term"],
                        "subjectCourse": elem["subjectCourse"],
                        "sequenceNumber": elem["sequenceNumber"],
                        "maximumEnrollment": elem["maximumEnrollment"],
                        "enrollment": elem["enrollment"],
                        "partOfTerm": elem["partOfTerm"]
                    }

                    processedData.append(dic)

print("Processing finished, outputting file to ./data")
print("Run the preprocess.py script to generate training data for the models")

with open("data/uniqueClassData.json", "w", encoding="utf8") as outfile:
    json.dump(processedData, outfile, indent = 4)
