from pandas import DataFrame, get_dummies,read_json

def pre_process(data) -> DataFrame:
    """Pre-processes JSON data for the ML model"""
    df_p = read_json("data/preReqData.json")

    df = DataFrame(data)
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
            # Number of offerings of the pre reqs in the previous semester
            if (df.at[j, "subjectCourse"] in preReqsList):
                df.at[i, "# prereqs prev sem"] += 1

            df.at[i,df.at[j, "subjectCourse"]] = 1

    df = get_dummies(df, columns=['subjectCourse','semester'])
    df.fillna(0, inplace=True, downcast="infer")
    df.to_csv("feature.csv",index=False)

    return df
