from argparse import ArgumentParser
from pandas import read_json, DataFrame, get_dummies


def pre_process() -> DataFrame:
    """Pre-processes raw JSON data for the ML method of Algorithm 2."""
    df = read_json("data/uniqueClassData.json")
    df_y = read_json("data/yearEnrollmentData.json")

    for i in df.index:
        
        for j in df.index:
           
            # Different course offered the same semester
            if df.at[i, "subjectCourse"] == df.at[j, "subjectCourse"]:
                df.at[i,df.at[j, "term"]] = df.at[j, "maximumEnrollment"]

    df.fillna(0, inplace=True, downcast="infer")
    df = df.reset_index(drop=True)
    df = df[df['sequenceNumber'].str.contains('A01')]
    df = df.drop_duplicates(subset=['subjectCourse'], keep='last')
    df = df.drop(columns=['sequenceNumber','maximumEnrollment','enrollment','term','id','partOfTerm'])

    cols = df.columns.tolist()
    cols[1:] = sorted(cols[1:])
    df=df[cols]

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

    df = pre_process()

    if args.xlsx:
        df.to_excel(args.xlsx + ".xlsx", index=False)
    if args.json:
        df.to_json(args.json + ".json", index=False)
    if args.csv:
        df.to_csv(args.csv + ".csv", index=False)


if __name__ == "__main__":
    main()
