from pandas import DataFrame, read_json, read_csv, get_dummies
from pickle import load
import json

def model_predict(data,df):
    """Predict capacity for coures subbmitted using a pretrained ML model"""
    preprocessed_df = read_json('app/models/data/training_data.json')

    preprocessed_df = preprocessed_df.loc[[0]]

    df = df.merge(preprocessed_df, how='left')
    # df = df.drop(columns=['seng_ratio', 'capacity'])

    df = df[preprocessed_df.drop(columns=['capacity']).columns]
    df.fillna(0, inplace=True, downcast="infer")

    ml_model_pkl = open('app/models/xgb_model.pkl', 'rb')
    ml_model = load(ml_model_pkl)

    result=ml_model.predict(df)
    # print(result,ml_model.apply(df))

    newcapacity_df=DataFrame(data)
    for i in newcapacity_df.index:
        if newcapacity_df.at[i,'capacity'] == 0:
            newcapacity_df.at[i,'capacity']=round(result[i])

    return newcapacity_df.to_json(orient="records")


