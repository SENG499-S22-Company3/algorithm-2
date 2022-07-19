from pickle import load
from pandas import DataFrame, read_json


def model_predict(data: list[dict], df: DataFrame) -> dict:
    """Predict capacity for courses submitted using a pre-trained ML model"""
    preprocessed_df = read_json("app/models/data/training_data.json")

    preprocessed_df = preprocessed_df.loc[[0]]

    df = df.merge(preprocessed_df, how="left")
    # df = df.drop(columns=["seng_ratio", "capacity"])

    df = df[preprocessed_df.drop(columns=["capacity"]).columns]
    df.fillna(0, inplace=True, downcast="infer")

    ml_model_pkl = open("app/models/xgb_model.pkl", "rb")
    ml_model = load(ml_model_pkl)

    result=ml_model.predict(df)
    # print(result,ml_model.apply(df))

    newcapacity_df = DataFrame(data)
    for i in newcapacity_df.index:
        if newcapacity_df.at[i, "capacity"] == 0:
            newcapacity_df.at[i, "capacity"]=round(result[i])

    return newcapacity_df.to_dict(orient="records")
