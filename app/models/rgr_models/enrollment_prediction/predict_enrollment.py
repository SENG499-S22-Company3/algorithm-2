"""Enrollment Predictor

This script takes any number of years as input and outputs a prediction of the number of the number
of students in each year of the BSEng program based on existing data (2014-2021).
"""
import os
import sys
import numpy as np
from argparse import ArgumentParser
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.join(os.path.dirname(__file__), "../data"))
from app.models.rgr_models.enrollment_prediction.enrollment_data import year_data

ENROLLMENT_DATA = sorted(year_data, key=lambda d: d["year"])

def predict_year_size(to_predict: list[int], keys: list[str]) -> np.ndarray:
    """Returns a prediction for the number of students for a given year and key."""
    years = list(range(ENROLLMENT_DATA[0]["year"], ENROLLMENT_DATA[-1]["year"] + 1))
    years = np.array(years).reshape(-1, 1)

    enrollment = []

    for year in ENROLLMENT_DATA:
        total = 0
        for key in keys:
            total += year[key]
        enrollment.append(total)

    enrollment = np.array(enrollment).reshape(-1, 1)


    predict_years = np.array(to_predict).reshape(-1, 1)

    model = LinearRegression()
    model.fit(years, enrollment)

    return model.predict(predict_years)


def predict_all_years(to_predict: list[int]) -> list[dict]:
    """Returns a list of dictionaries with the predicted enrollment numbers for the provided
    years."""
    first_year = predict_year_size(to_predict, ["1stYear"])
    second_year = predict_year_size(to_predict, ["2ndYear", "2ndYearTransfer"])
    third_year = predict_year_size(to_predict, ["3rdYear"])
    fourth_year = predict_year_size(to_predict, ["4thYear", "5thYear", "6thYear", "7thYear"])

    output = []
    for i, year in enumerate(to_predict):
        entry = {
            "year": year,
            "1stYear": int(first_year[i][0]),
            "2ndYear": int(second_year[i][0]),
            "3rdYear": int(third_year[i][0]),
            "4thYear": int(fourth_year[i][0]),
        }
        output.append(entry)

    return output


def main():
    """Main function."""
    parser = ArgumentParser(description="Enrollment Predictor")
    parser.add_argument("years", type=int, nargs="+", help="years to predict")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided.")

    print(predict_all_years(args.years))


if __name__ == "__main__":
    main()
