from pandas import DataFrame, read_json, read_csv, get_dummies
from pickle import load
import json
from pathlib import Path,PurePath

def model_predict(data,df):
    """Predict capacity for coures subbmitted using a pretrained ML model"""
    root=PurePath(__file__).parents[0]

    preprocessed_df = read_json(str(root) + "/ml_models/data/training_data.json")
    preprocessed_df = preprocessed_df.loc[[0]]

    df = df.merge(preprocessed_df, how='left')
    # df = df.drop(columns=['seng_ratio', 'capacity'])

    df = df[preprocessed_df.drop(columns=['capacity']).columns]
    df.fillna(0, inplace=True, downcast="infer")

    ml_model_pkl = open(str(root) + "/ml_models/xgb_model.pkl", 'rb')
    ml_model = load(ml_model_pkl)

    result=ml_model.predict(df)
    # print(result,ml_model.apply(df))

    newcapacity_df=DataFrame(data)
    for i in newcapacity_df.index:
        subjectCourse=str(newcapacity_df.at[i,'subject'] + newcapacity_df.at[i,'code'])

        #couse has been seen by ML model
        if subjectCourse in course_list:
            if newcapacity_df.at[i,'capacity'] == 0:
                newcapacity_df.at[i,'capacity']=abs(round(result[i]))

                #check to see if capacity is valid
                for j in capacity_df.index:
                    if all([
                        subjectCourse == capacity_df.at[j, 'subjectCourse'],
                        newcapacity_df.at[i,'semester'] == capacity_df.at[j, 'semester']
                    ]):
                        if newcapacity_df.at[i,'capacity'] > capacity_df.at[j, 'capacity']*1.25 or \
                        newcapacity_df.at[i,'capacity'] < capacity_df.at[j, 'capacity']*0.75:
                            newcapacity_df.at[i,'capacity'] = capacity_df.at[j, 'capacity']

        else:
            #course is not hardcoded into the schedule
            if subjectCourse not in hardcoded_course_list:
                if newcapacity_df.at[i,'capacity'] == 0:
                    newcapacity_df.at[i,'capacity'] = 80


    return newcapacity_df.to_dict(orient="records")
