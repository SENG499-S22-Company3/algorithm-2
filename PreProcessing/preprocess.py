from argparse import ArgumentParser
import pandas as pd
from pathlib import PurePath

def pre_process(df) -> pd.DataFrame:
    """Pre-processes raw JSON data for the ML method of Algorithm 2."""

    print('Preprocessing...')

    df = df.drop(columns=['id','maximumEnrollment', 'term'])

    df = pd.get_dummies(data=df, columns=['subjectCourse','semester'])
    return df


def main() -> None:
    """Main function."""
    parser = ArgumentParser(description="Preprocessing for algorithm 2 - ML method")
    parser.add_argument("-x", action="store", dest="xlsx", help="output data frame to .xlsx")
    parser.add_argument("-j", action="store", dest="json", help="output data frame to .json")
    parser.add_argument("-c", action="store", dest="csv", help="output data frame to .csv")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided.")


    if args.xlsx:
        df = pd.read_excel(args.xlsx + ".xlsx")
    if args.json:
        df = pd.read_json(args.json + ".json")
    if args.csv:
        df = pd.read_csv(args.csv + ".csv")

    root=PurePath(__file__).parents[1]

    preprocessed_df = pre_process(df.copy())

    if args.xlsx:
        preprocessed_df.to_excel(str(root) + "/Modeling/" + "preprocessed_" + args.xlsx.split("/")[-1] + ".xlsx", index=False)
    if args.json:
        preprocessed_df.to_json(str(root) + "/Modeling/" +"preprocessed_" + args.json.split("/")[-1] + ".json", index=False)
    if args.csv:
        preprocessed_df.to_csv(str(root) + "/Modeling/" + "preprocessed_" + args.csv.split("/")[-1] + ".csv", index=False)





if __name__ == "__main__":
    main()
