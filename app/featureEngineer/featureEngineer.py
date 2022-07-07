from pandas import DataFrame, get_dummies

def pre_process(data) -> DataFrame:
    """Pre-processes JSON data for the ML model"""

    df = DataFrame(data)
    df["subjectCourse"] = df["subject"].astype(str)  + df["code"].astype(str)
    df = df.drop(columns = ['subject', 'code'])

    df = df.reset_index(drop=True)
    for i in df.index:
        for j in df.index:
                df.at[i,df.at[j, "subjectCourse"]] = 1

    df = get_dummies(df, columns=['subjectCourse','semester'])
    df.fillna(0, inplace=True, downcast="infer")

    return df
