from argparse import ArgumentParser
import pandas as pd


def pre_process(df) -> pd.DataFrame:
    """Pre-processes raw JSON data for the ML method of Algorithm 2."""
    
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

    preprocessed_df = pre_process(df.copy())

    if args.xlsx:
        df.to_excel("preprocessed_" + args.xlsx.split("/")[-1] + ".xlsx", index=False)
    if args.json:
        df.to_json("preprocessed_" + args.json.split("/")[-1] + ".json", index=False)
    if args.csv:
        df.to_csv("preprocessed_" + args.csv.split("/")[-1] + ".csv", index=False)


        


if __name__ == "__main__":
    main()
