from argparse import ArgumentParser
from pandas import read_json, DataFrame
from pathlib import PurePath

def pre_process() -> DataFrame:
    """Pre-processes raw JSON data for the ML method of Algorithm 2."""
    print('Feature engineering...')

    df = read_json("data/uniqueClassData.json")
    df_y = read_json("data/yearEnrollmentData.json")

    df = df.assign(**{"semester":'', "# Offerings":1,"isBefore2014": 1, "# Y1": 0, "# Y2": 0,"# Y3": 0,"# Y4": 0,"# Y5+": 0})

    for i in df.index:
        year = int(str(df.at[i, "term"])[:-2])
        semester = int(str(df.at[i, "term"])[-2:])
        if semester in (1, 5):
            year = year - 1

        match semester:
            case 1:
                df.at[i, "semester"] = 'Spring'
            case 5:
                df.at[i, "semester"] = 'Summer'
            case 9:
                df.at[i, "semester"] = 'Fall'

        # Number of SENG students by year when the course is offered
        if int(df.at[i, "term"]) >= 201409:
            df.at[i, "# Y1"] = df_y[df_y["year"] == year]["1stYear"].values[0]
            df.at[i, "# Y2"] = df_y[df_y["year"] == year]["2ndYear"].values[0] + \
                               df_y[df_y["year"] == year]["2ndYearTransfer"].values[0]
            df.at[i, "# Y3"] = df_y[df_y["year"] == year]["3rdYear"].values[0]
            df.at[i, "# Y4"] = df_y[df_y["year"] == year]["4thYear"].values[0]
            df.at[i, "# Y5+"] = df_y[df_y["year"] == year]["5thYear"].values[0] + \
                                df_y[df_y["year"] == year]["6thYear"].values[0] + \
                                df_y[df_y["year"] == year]["7thYear"].values[0]
            df.at[i, "isBefore2014"] = 0

        for j in df.index:
            year2 = int(str(df.at[j, "term"])[:-2])
            semester2 = int(str(df.at[j, "term"])[-2:])

            if semester2 in (1, 5):
                year2 = year2-1

            # Number of times course is offered in an academic year
            if all([
                year == year2,
                df.at[i, "subjectCourse"] == df.at[j, "subjectCourse"],
                df.at[j, "sequenceNumber"] == "A01",
                str(df.at[i, "term"]) != str(df.at[j, "term"])
            ]):
                df.at[i, "# Offerings"] = df.at[i, "# Offerings"] + 1

            # Computes the total maximumEnrollment and enrollment for A01 section
            if all([
                df.at[i, "term"] == df.at[j, "term"],
                df.at[i, "subjectCourse"] == df.at[j, "subjectCourse"],
                df.at[i, "sequenceNumber"] == "A01",
                df.at[j, "sequenceNumber"] != "A01"
            ]):
                df.at[i, "maximumEnrollment"] =  df.at[i, "maximumEnrollment"] +  df.at[j, "maximumEnrollment"]
                df.at[i, "enrollment"] =  df.at[i, "enrollment"] +  df.at[j, "enrollment"]

            # Different course offered the same semester
            if df.at[i, "term"] == df.at[j, "term"]:
                df.at[i,df.at[j, "subjectCourse"]] = 1

    df.fillna(0, inplace=True, downcast="infer")
    df = df.reset_index(drop=True)
    df=df[df['sequenceNumber'].str.contains('A01')]
    df=df.drop(columns=['sequenceNumber'])
    return df


def main() -> None:
    """Main function."""
    parser = ArgumentParser(description="Feature Engineering for algorithm 2 - ML method")
    parser.add_argument("-x", action="store", dest="xlsx", help="output data frame to .xlsx")
    parser.add_argument("-j", action="store", dest="json", help="output data frame to .json")
    parser.add_argument("-c", action="store", dest="csv", help="output data frame to .csv")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided.")

    root=PurePath(__file__).parents[1]

    df = pre_process()

    if args.xlsx:
        df.to_excel(str(root) + "/PreProcessing/" + args.xlsx + ".xlsx", index=False)
    if args.json:
        df.to_json(str(root) + "/PreProcessing/" + args.json + ".json", index=False)
    if args.csv:
        df.to_csv(str(root) + "/PreProcessing/" + args.csv + ".csv", index=False)


if __name__ == "__main__":
    main()