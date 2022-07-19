import csv
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from xgboost import XGBRegressor
from argparse import ArgumentParser
from sklearn import svm, tree
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def optimize_dt(df: pd.DataFrame) -> tree.DecisionTreeRegressor:
    print("Creating Decision Tree...")

    # create a regressor object
    X = df.drop(columns=["capacity"])

    y = df[["capacity"]]

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

    # fig = plt.figure(figsize=(60,45))
    # tree.plot_tree(model,
    #                feature_names=X.columns,
    #                filled=True)
    # plt.savefig("tree.png")
    return model

def optimize_svm(df: pd.DataFrame) -> svm.SVR:
    print("Creating Decision Tree...")

    # create a regressor object
    X = df.drop(columns=["capacity"])
    y = df[["capacity"]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=11)


    model = svm.SVR(kernel="linear")
    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print(f"Train MAE: {mean_absolute_error(y_train_pred, y_train)}")
    print(f"Test MAE: {mean_absolute_error(y_test_pred, y_test)}")

    # fig = plt.figure(figsize=(60,45))
    # tree.plot_tree(model,
    #                feature_names=X.columns,
    #                filled=True)
    # plt.savefig("tree.png")
    return model

def optimize_xgb(df: pd.DataFrame) -> None:
    print("Starting Optimization")

    # create a regressor object
    X = df.drop(columns=["capacity"])
    y = df[["capacity"]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=15)

    gamma_vals = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    learning_rate_vals = [0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
    max_depth_vals = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    reg_alpha_vals = [0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]

    min_mae = 100
    with open("data/optimization_results.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(["TrainMAE", "TestMAE", "Gamma", "LearningRate", "MaxDepth", "RegAlpha"])

        for i in tqdm(range(0, len(gamma_vals))):
            for j in range(0, len(learning_rate_vals)):
                for k in range(0, len(max_depth_vals)):
                    for l in range(0, len(reg_alpha_vals)):
                        model = XGBRegressor(gamma=gamma_vals[i],
                                             learning_rate=learning_rate_vals[j],
                                             max_depth=max_depth_vals[k],
                                             n_estimators=5000,
                                             random_state=20,
                                             reg_alpha =reg_alpha_vals[l])

                        # fit the regressor with X and Y data
                        model.fit(X_train, y_train)

                        y_train_pred = model.predict(X_train)
                        y_test_pred = model.predict(X_test)

                        train_mae = mean_absolute_error(y_train_pred, y_train)
                        test_mae = mean_absolute_error(y_test_pred, y_test)

                        w.writerow([train_mae, test_mae, gamma_vals[i], learning_rate_vals[j],
                                    max_depth_vals[k], reg_alpha_vals[l]])

                        if(test_mae < min_mae):
                            min_mae = test_mae
                            print(f"New min mae: {min_mae}, "
                                  f"Gamma: {gamma_vals[i]}, "
                                  f"learning_rate: {learning_rate_vals[j]}, "
                                  f"max_depth: {max_depth_vals[k]}, "
                                  f"reg_alpha: {reg_alpha_vals[l]}")

    return

def optimize_rf(df: pd.DataFrame) -> None:
    print("Creating Random Forest Model...")

    # create a regressor object
    X = df.drop(columns=["capacity"])
    y = df[["capacity"]]

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

    fig = plt.figure(figsize=(60, 45))
    tree.plot_tree(model.estimators_[0],
                   feature_names=X.columns,
                   filled=True)
    plt.savefig("rf_tree.png")

    return


def main() -> None:
    """Main function."""
    parser = ArgumentParser(description="Preprocessing for algorithm 2 - ML method")
    parser.add_argument("-xgb", action="store_true", dest="xgb", help="Train gradient boost model")
    parser.add_argument("-rf", action="store_true", dest="rf", help="Train random forest model")
    parser.add_argument("-dt", action="store_true", dest="dt", help="Train decision tree model")
    parser.add_argument("-svm", action="store_true", dest="svm", help="Train SVM model")
    parser.add_argument("-x", action="store_true", dest="xlsx", help="output data frame to .xlsx")
    parser.add_argument("-j", action="store_true", dest="json", help="output data frame to .json")
    parser.add_argument("-c", action="store_true", dest="csv", help="output data frame to .csv")

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
        optimize_xgb(df.copy())
    if args.rf:
        optimize_rf(df.copy())
    if args.dt:
        optimize_dt(df.copy())
    if args.svm:
        optimize_svm(df.copy())

    print("Optimiation Finished")

if __name__ == "__main__":
    main()
