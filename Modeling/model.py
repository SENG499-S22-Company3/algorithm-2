import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn import tree
  



def train_model(df):
    # create a regressor object
    X = df.drop(columns=['enrollment', 'partOfTerm'])
    y = df[['enrollment']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=11)


    model = tree.DecisionTreeRegressor(criterion='squared_error',
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

    fig = plt.figure(figsize=(25,20))
    tree.plot_tree(model, 
                   feature_names=X.columns,  
                   filled=True)
    plt.show()


    





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

    


        


if __name__ == "__main__":
    main()
