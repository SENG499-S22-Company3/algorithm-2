from pandas import DataFrame, get_dummies

def pre_process(data) -> DataFrame:
    """Pre-processes JSON data for the ML method of Algorithm 2."""

    df = DataFrame(data)
    df = df.assign(**{"enrollment":0})
    df= df.explode("courses_to_predict")
    print(df)

    df = df.reset_index(drop=True)
    for i in df.index:
        for j in df.index:
            # Different course offered the same semester
            if str(df.at[i, "semester"]) == str(df.at[j, "semester"]):
                df.at[i,df.at[j, "courses_to_predict"]] = 1

    df.fillna(0, inplace=True, downcast="infer")
    df = get_dummies(data=df, columns=['courses_to_predict','semester'])
    return (df)
