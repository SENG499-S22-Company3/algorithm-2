from pandas import DataFrame, read_json, read_csv, get_dummies
from pickle import load
import json

course_list=[
    "CSC111",
    "CSC115",
    "CSC225",
    "CSC226",
    "CSC230",
    "CSC320",
    "CSC360",
    "CSC361",
    "CSC370",
    "ECE300",
    "ECE310",
    "ECE320",
    "ECE330",
    "ECE340",
    "ECE360",
    "ECE455",
    "ECE458",
    "ECE488",
    "SENG265",
    "SENG275",
    "SENG310",
    "SENG321",
    "SENG371",
    "SENG401",
    "SENG468",
    "SENG474",
    "CSC355",
    "ECE216",
    "ECE241",
    "ECE250",
    "ECE255",
    "ECE260",
    "ECE350",
    "ECE355",
    "ECE356",
    "ECE365",
    "ECE370",
    "ECE380",
    "ECE399",
    "ECE403",
    "ECE463",
    "SENG350",
    "SENG360",
    "ECE220",
    "ECE242",
    "ECE299",
    "ECE410",
    "ECE499",
    "SENG426",
    "SENG440",
    "SENG499",
    "CSC460",
    "SENG411",
    "SENG421",
    "SENG435",
    "SENG466"
]

hardcoded_course_list=[
    "MATH122",
    "ENGR002",
    "MATH109",
    "MATH100",
    "MATH110",
    "ENGR130",
    "ENGR110",
    "PHYS110",
    "MATH101",
    "ENGR120",
    "ENGR141",
    "PHYS111",
    "ENGR001",
    "CHEM101",
    "CHEM150",
    "STAT260",
    "ECON180",
    "ENGR003",
    "ENGR004"]

def model_predict(data,df):
    """Predict capacity for coures subbmitted using a pretrained ML model"""
    preprocessed_df = read_json('app/models/data/training_data.json')
    capacity_df = read_json('app/models/data/capacity_data.json')

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
        subjectCourse=str(newcapacity_df.at[i,'subject'] + newcapacity_df.at[i,'code'])

        #couse has been seen by ML model
        if subjectCourse in course_list:
            if newcapacity_df.at[i,'capacity'] == 0:
                newcapacity_df.at[i,'capacity']=round(result[i])
                
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


