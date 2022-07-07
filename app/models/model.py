from pickle import load
from pandas import DataFrame, read_json, get_dummies


def model_predict(data,df):
    """Predict capacity for courses submitted using a pre-trained ML model"""
    preprocessed_df = read_json("app/models/data/training_data.json")
    preprocessed_df = get_dummies(preprocessed_df, columns=["subjectCourse", "semester"])
    preprocessed_df = preprocessed_df.loc[[0]]

    df = df.merge(preprocessed_df, how="left")
    df = df.drop(columns=["seng_ratio", "capacity"])
    df.fillna(0, inplace=True, downcast="infer")

    with open("app/models/dt_model.pkl", "rb") as ml_model_pkl:
        ml_model = load(ml_model_pkl)

    result=ml_model.predict(df)

    newcapacity_df=DataFrame(data)
    for i in newcapacity_df.index:
        if newcapacity_df.at[i, "capacity"] == 0:
            newcapacity_df.at[i, "capacity"]=round(result[i])

    return newcapacity_df.to_json(orient="records")
