import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import csv
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn import tree, preprocessing
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path,PurePath
from xgboost import XGBRegressor
from sklearn import svm
from tqdm import tqdm
import time

def optimize_dt(df):
    print('Optimizing DT model')

    # create a regressor object
    X = df.drop(columns=['capacity'])
    
    y = df[['capacity']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=11)

    model = tree.DecisionTreeRegressor(criterion='squared_error',
                    max_depth=30,
                    max_leaf_nodes=60,
                    min_samples_leaf=3,
                    random_state=11)

    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    min_mae = 100
    with open('data/dt_optimization_results.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['TrainMAE', 'TestMAE', 'Gamma', 'LearningRate', 'MaxDepth', 'RegAlpha'])

        for i in tqdm(range(0,len(gamma_vals))):
            for j in range(0,len(learning_rate_vals)):
                for k in range(0,len(max_depth_vals)):
                    for l in range(0,len(reg_alpha_vals)):
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

                        w.writerow([train_mae, test_mae, gamma_vals[i], learning_rate_vals[j], max_depth_vals[k], reg_alpha_vals[l]])

                        if(test_mae < min_mae):
                            min_mae = test_mae
                            print(f"New min mae: {min_mae}, Gamma: {gamma_vals[i]}, learning_rate: {learning_rate_vals[j]}, max_depth: {max_depth_vals[k]}, reg_alpha: {reg_alpha_vals[l]}")
    return

def optimize_svm(df):
    print('Optimizing SVM model')

    # create a regressor object
    X = df.drop(columns=['capacity'])
    y = df[['capacity']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=11)

    
    model = svm.SVR(kernel="linear")
    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    min_mae = 100
    with open('data/svm_optimization_results.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['TrainMAE', 'TestMAE', 'Gamma', 'LearningRate', 'MaxDepth', 'RegAlpha'])

        for i in tqdm(range(0,len(gamma_vals))):
            for j in range(0,len(learning_rate_vals)):
                for k in range(0,len(max_depth_vals)):
                    for l in range(0,len(reg_alpha_vals)):
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

                        w.writerow([train_mae, test_mae, gamma_vals[i], learning_rate_vals[j], max_depth_vals[k], reg_alpha_vals[l]])

                        if(test_mae < min_mae):
                            min_mae = test_mae
                            print(f"New min mae: {min_mae}, Gamma: {gamma_vals[i]}, learning_rate: {learning_rate_vals[j]}, max_depth: {max_depth_vals[k]}, reg_alpha: {reg_alpha_vals[l]}")
    return

def optimize_xgb(df):
    print('Optimizing XGB model')

    # create a regressor object
    X = df.drop(columns=['capacity'])
    y = df[['capacity']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=15)

    gamma_vals = [4,4.5,5,5.5,6]
    learning_rate_vals = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
    max_depth_vals = [12,14,16,18,20]
    reg_alpha_vals = [0.1, 0.5, 1, 1.5, 2]

    min_mae = 100
    with open('data/xgb_optimization_results.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['TrainMAE', 'TestMAE', 'Gamma', 'LearningRate', 'MaxDepth', 'RegAlpha'])

        for i in tqdm(range(0,len(gamma_vals))):
            for j in range(0,len(learning_rate_vals)):
                for k in range(0,len(max_depth_vals)):
                    for l in range(0,len(reg_alpha_vals)):
                        model = XGBRegressor(gamma=gamma_vals[i],
                        learning_rate=learning_rate_vals[j],
                        max_depth=max_depth_vals[k],
                        n_estimators=10000,
                        random_state=20,
                        reg_alpha = reg_alpha_vals[l])

                        # fit the regressor with X and Y data
                        model.fit(X_train, y_train)

                        y_train_pred = model.predict(X_train)
                        y_test_pred = model.predict(X_test)

                        train_mae = mean_absolute_error(y_train_pred, y_train)
                        test_mae = mean_absolute_error(y_test_pred, y_test)

                        w.writerow([train_mae, test_mae, gamma_vals[i], learning_rate_vals[j], max_depth_vals[k], reg_alpha_vals[l]])

                        if(test_mae < min_mae):
                            min_mae = test_mae
                            print(f"New min mae: {min_mae}, Gamma: {gamma_vals[i]}, learning_rate: {learning_rate_vals[j]}, max_depth: {max_depth_vals[k]}, reg_alpha: {reg_alpha_vals[l]}")
    return

def optimize_rf(df):
    print('Optimizing RF model')

    # create a regressor object
    X = df.drop(columns=['capacity'])
    y = df[['capacity']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=15)

    model = RandomForestRegressor(criterion='squared_error',
                    max_depth=10,
                    max_leaf_nodes=30,
                    min_samples_leaf=5,
                    random_state=15)

    # fit the regressor with X and Y data
    print("Training Model...")
    model.fit(X_train, y_train)

    min_mae = 100
    with open('data/rf_optimization_results.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['TrainMAE', 'TestMAE', 'Gamma', 'LearningRate', 'MaxDepth', 'RegAlpha'])

        for i in tqdm(range(0,len(gamma_vals))):
            for j in range(0,len(learning_rate_vals)):
                for k in range(0,len(max_depth_vals)):
                    for l in range(0,len(reg_alpha_vals)):
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

                        w.writerow([train_mae, test_mae, gamma_vals[i], learning_rate_vals[j], max_depth_vals[k], reg_alpha_vals[l]])

                        if(test_mae < min_mae):
                            min_mae = test_mae
                            print(f"New min mae: {min_mae}, Gamma: {gamma_vals[i]}, learning_rate: {learning_rate_vals[j]}, max_depth: {max_depth_vals[k]}, reg_alpha: {reg_alpha_vals[l]}")
    return

def main() -> None:
    """Main function."""
    """
    parser = ArgumentParser(description="Preprocessing for algorithm 2 - ML method")
    parser.add_argument("-xgb", action="store_true", dest="xgb", help="Train gradient boost model")
    parser.add_argument("-rf", action="store_true", dest="rf", help="Train random forest model")
    parser.add_argument("-dt", action="store_true", dest="dt", help="Train decesion tree model")
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

    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

    if args.xgb:
        optimize_xgb(df.copy())
    if args.rf:
        optimize_rf(df.copy())
    if args.dt:
        optimize_dt(df.copy())
    if args.svm:
        optimize_svm(df.copy())
    """

    df = pd.read_json("data/training_data.json")
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

    optimize_xgb(df.copy())
    optimize_rf(df.copy())
    optimize_dt(df.copy())
    optimize_svm(df.copy())

    print("Optimization Finished")

if __name__ == "__main__":
    main()
