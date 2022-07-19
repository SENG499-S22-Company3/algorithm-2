from pandas import DataFrame, get_dummies,read_json
import os

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

def pre_process(data) -> DataFrame:
    """Pre-processes JSON data for the ML model"""
    
    df_p = read_json("app/featureEngineer/data/preReqData.json")

    df = DataFrame(data)

    df = df.assign(**{"# prereqs prev sem":0,"# Offerings":1})
    df["subjectCourse"] = df["subject"].astype(str)  + df["code"].astype(str)
    df = df.drop(columns = ['subject', 'code'])

    df = df.reset_index(drop=True)

    for i in df.index:
        if df.at[i, "subjectCourse"] not in course_list:
            df.drop([i])
        else:
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