from argparse import ArgumentParser
import pandas as pd
from pathlib import PurePath

def pre_process() -> pd.DataFrame:
    """Pre-processes raw JSON data for the ML method of Algorithm 2."""
    df_c = pd.read_json("../FeatureEngineering/data/uniqueClassData.json")
    df_y = pd.read_json("../FeatureEngineering/data/yearEnrollmentData.json")
    df_p = pd.read_json("../FeatureEngineering/data/preReqData.json")

    df_c = df_c.assign(**{"# Offerings":1, "# prereqs":0, "# prereqs prev sem":0,"# students in prereqs":0, "# Y1": 0, "# Y2": 0,"# Y3": 0,"# Y4": 0,"# Y5+": 0})

    for i in df_c.index:
        year = int(str(df_c.at[i, "term"])[:-2])
        semester = int(str(df_c.at[i, "term"])[-2:])
        # If spring or summer semester, its part of the previous academic year
        if semester in (5, 9):
            semester = 0
        elif semester in (1,5):
            semester = 1
            year = year - 1
        else:
            semester = 2
            year = year - 1

        # Get the list of prereqs for this course
        preReqsIndex = df_p[df_p['course'] == df_c.at[i, "subjectCourse"]].reset_index()
        preReqsList = preReqsIndex.at[0, "preReqs"]
        numPreReqs = len(preReqsList)

        # Set the number of pre reqs
        df_c.at[i, "# pre reqs"] = len(preReqsIndex.at[0, "preReqs"])

        # Number of SENG students by year when the course is offered
        if year >= 2014 and year <= 2021:
            df_c.at[i, "# Y1"] = df_y[df_y["year"] == year]["1stYear"].values[0]
            df_c.at[i, "# Y2"] = df_y[df_y["year"] == year]["2ndYear"].values[0] + \
                               df_y[df_y["year"] == year]["2ndYearTransfer"].values[0]
            df_c.at[i, "# Y3"] = df_y[df_y["year"] == year]["3rdYear"].values[0]
            df_c.at[i, "# Y4"] = df_y[df_y["year"] == year]["4thYear"].values[0]
            df_c.at[i, "# Y5+"] = df_y[df_y["year"] == year]["5thYear"].values[0] + \
                                df_y[df_y["year"] == year]["6thYear"].values[0] + \
                                df_y[df_y["year"] == year]["7thYear"].values[0]

        for j in df_c.index:
            year2 = int(str(df_c.at[j, "term"])[:-2])
            semester2 = int(str(df_c.at[j, "term"])[-2:])

            if semester2 in (5, 9):
                semester2 = 0
            elif semester2 in (1,5):
                semester2 = 1
                year2 = year2 - 1
            else:
                semester2 = 2
                year2 = year2 - 1

            # Number of times course is offered in an academic year
            if all([
                year == year2,
                df_c.at[i, "subjectCourse"] == df_c.at[j, "subjectCourse"],
                df_c.at[j, "sequenceNumber"] == "A01",
                str(df_c.at[i, "term"]) != str(df_c.at[j, "term"])
            ]):
                df_c.at[i, "# Offerings"] = df_c.at[i, "# Offerings"] + 1

            # Number of offerings of the pre reqs in the previous semester
            if((year == year2) and (semester == (semester2 - 1))) or \
            ((year == (year2 - 1)) and ((semester == 0 and semester2 == 2))):
                if df_c.at[j, "subjectCourse"] in preReqsList:
                    df_c.at[i, "# prereqs prev sem"] += 1
                    df_c.at[i, "# students in prereqs"] += df_c.at[j, "enrollment"]

            # Different course offered the same semester
            if df_c.at[i, "term"] == df_c.at[j, "term"]:
                df_c.at[i,df_c.at[j, "subjectCourse"]] = 1

    df_c.fillna(0, inplace=True, downcast="infer")
    df_c = df_c.reset_index(drop=True)
    return df_c

def main() -> None:
    """Main function."""
    parser = ArgumentParser(description="Preprocessing for algorithm 2 - ML method")
    parser.add_argument("-x", action="store_true", dest="xlsx", help="output data frame to .xlsx")
    parser.add_argument("-j", action="store_true", dest="json", help="output data frame to .json")
    parser.add_argument("-c", action="store_true", dest="csv", help="output data frame to .csv")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided.")

    root=PurePath(__file__).parents[1]

    preprocessed_df = pre_process()

    if args.xlsx:
        preprocessed_df.to_excel(str(root) + "/Modeling/" + "preprocessed_data" + ".xlsx")
    if args.json:
        preprocessed_df.to_json(str(root) + "/Modeling/" +"preprocessed_data" + ".json")
    if args.csv:
        preprocessed_df.to_csv(str(root) + "/Modeling/" + "preprocessed_data" + ".csv")

if __name__ == "__main__":
    main()
