from pandas import DataFrame, get_dummies,read_json
import os

def pre_process(data) -> DataFrame:
    """Pre-processes JSON data for the ML model"""
    print("Reading input data")
  
    df_p = read_json("app/featureEngineer/data/preReqData.json")

    df = DataFrame(data)
    
    df = df.assign(**{"# prereqs prev sem":0,"# Offerings":1})
    df["subjectCourse"] = df["subject"].astype(str)  + df["code"].astype(str)
    df = df.drop(columns = ['subject', 'code'])

    df = df.reset_index(drop=True)

    for i in df.index:
         # Get the list of prereqs for this course
        preReqsIndex = df_p[df_p['course'] == df.at[i, "subjectCourse"]].reset_index()
        preReqsList = preReqsIndex.at[0, "preReqs"]

        # Set the number of pre reqs
        df.at[i, "# prereqs"] = len(preReqsList)
        
        for j in df.index:
            if all([
                str(df.at[i, "semester"]) == str(df.at[j, "semester"]),
                df.at[i, "subjectCourse"] == df.at[j, "subjectCourse"]
            ]):
                df.at[i, "# Offerings"] = df.at[i, "# Offerings"] + 1

            # Number of offerings of the pre reqs in the previous semester
            if (df.at[j, "subjectCourse"] in preReqsList):
                df.at[i, "# prereqs prev sem"] += 1

            df.at[i,df.at[j, "subjectCourse"]] = 1

    df = get_dummies(df, columns=['subjectCourse','semester'])
    df.fillna(0, inplace=True, downcast="infer")
    # df.to_csv("feature.csv",index=False)

    return df