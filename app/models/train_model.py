import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from argparse import ArgumentParser


def train_model_dt(df: pd.DataFrame) -> tree.DecisionTreeRegressor:
    print("Creating Decision Tree...")

    # create a regressor object
    X = df.drop(columns=["capacity"])
    y = df[["capacity"]]

    # One hot encode
    X = pd.get_dummies(X, columns=["subjectCourse", "semester"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=11)

    model = tree.DecisionTreeRegressor(criterion="squared_error",
                                       max_depth=30,
                                       max_leaf_nodes=60,
                                       min_samples_leaf=3,
                                       random_state=11)

    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print(f"Train MAE: {mean_absolute_error(y_train_pred, y_train)}")
    print(f"Test MAE: {mean_absolute_error(y_test_pred, y_test)}")

    fig = plt.figure(figsize=(60, 45))
    tree.plot_tree(model,
                   feature_names=X.columns,
                   filled=True)
    plt.savefig("tree.png")
    return model


def train_model_xgb(df: pd.DataFrame) -> XGBRegressor:
    print("Creating Gradient Boosted Decision Tree Model...")

    # create a regressor object
    X = df.drop(columns=["capacity"])
    y = df[["capacity"]]

    # One hot encode
    X = pd.get_dummies(X, columns=["subjectCourse", "semester"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=15)

    model = XGBRegressor(gamma=10,
                         learning_rate=0.01,
                         max_depth=10,
                         n_estimators=10000,
                         subsample=0.8,
                         random_state=20,
                         reg_alpha=0.3)

    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print(f"Train MAE: {mean_absolute_error(y_train_pred, y_train)}")
    print(f"Test MAE: {mean_absolute_error(y_test_pred, y_test)}")

    """
    fig = plt.figure(figsize=(60,45))
    tree.plot_tree(model,
                   feature_names=X.columns,
                   filled=True)
    plt.savefig("xgb_tree.png")
    """

    return model


def train_model_rf(df: pd.DataFrame):
    print("Creating Random Forest Model...")

    # create a regressor object
    X = df.drop(columns=["capacity"])
    y = df[["capacity"]]

    # One hot encode
    X = pd.get_dummies(X, columns=["subjectCourse", "semester"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=15)

    model = RandomForestRegressor(criterion="squared_error",
                                  max_depth=10,
                                  max_leaf_nodes=30,
                                  min_samples_leaf=5,
                                  random_state=15)

    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print(f"Train MAE: {mean_absolute_error(y_train_pred, y_train)}")
    print(f"Test MAE: {mean_absolute_error(y_test_pred, y_test)}")

    fig = plt.figure(figsize=(60,45))
    tree.plot_tree(model.estimators_[0],
                   feature_names=X.columns,
                   filled=True)
    plt.savefig("rf_tree.png")

    return model


def main() -> None:
    """Main function."""
    parser = ArgumentParser(description="Preprocessing for algorithm 2 - ML method")
    parser.add_argument("-xgb", action="store_true", dest="xgb", help="Train gradient boost model")
    parser.add_argument("-rf", action="store_true", dest="rf", help="Train random forest model")
    parser.add_argument("-dt", action="store_true", dest="dt", help="Train decision tree model")
    parser.add_argument("-x", action="store_true", dest="xlsx", help="Output data frame to .xlsx")
    parser.add_argument("-j", action="store_true", dest="json", help="Output data frame to .json")
    parser.add_argument("-c", action="store_true", dest="csv", help="Output data frame to .csv")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided.")

    if args.xlsx:
        df = pd.read_excel("data/training_data.xlsx")
    if args.json:
        df = pd.read_json("data/training_data.json")
    if args.csv:
        df = pd.read_csv("data/training_data.csv")

    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    if args.xgb:
        model = train_model_xgb(df.copy())
        model_name = "xgb_model.pkl"
    if args.rf:
        model = train_model_rf(df.copy())
        model_name = "rf_model.pkl"
    if args.dt:
        model = train_model_dt(df.copy())
        model_name = "dt_model.pkl"

    print("Training finished. Outputting pickle file for model.")

    with open(model_name, "wb") as model_file:
        pickle.dump(model, model_file)


if __name__ == "__main__":
    main()
