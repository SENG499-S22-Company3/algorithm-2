import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn import tree, preprocessing
from pathlib import Path,PurePath

def train_model(df):
    print('Creating Decision Tree...')

    # create a regressor object
    X = df.drop(columns=['enrollment', 'partOfTerm'])
    y = df[['enrollment']]

    # Label encoder for subjectCourse
    le_sc = preprocessing.LabelEncoder()
    le_sc.fit(X["subjectCourse"])
    X["subjectCourse"] = le_sc.transform(X["subjectCourse"])

    # Label encoder for sequenceNumber
    le_sn = preprocessing.LabelEncoder()
    le_sn.fit(X["sequenceNumber"])
    X["sequenceNumber"] = le_sn.transform(X["sequenceNumber"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=15)

    model = tree.DecisionTreeRegressor(criterion='squared_error',
                    max_depth=10,
                    max_leaf_nodes=30,
                    min_samples_leaf=3,
                    random_state=15)

    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print(f"Train MAE: {mean_absolute_error(y_train_pred, y_train)}")
    print(f"Test MAE: {mean_absolute_error(y_test_pred, y_test)}")

    fig = plt.figure(figsize=(60,45))
    tree.plot_tree(model,
                   feature_names=X.columns,
                   filled=True)
    plt.savefig('tree.png')


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

    model = train_model(df.copy())

    with open('model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    root=PurePath(__file__).parents[1]
    # Delete if it already exists
    try:
        os.remove(str(root)+"/app/models/model.pkl")
    except OSError:
        pass

    Path("./model.pkl").rename(str(root)+"/app/models/model.pkl")

if __name__ == "__main__":
    main()
