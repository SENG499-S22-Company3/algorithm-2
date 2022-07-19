import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

xAxisTicks = []
for i in range(0, 450, 50):
    xAxisTicks.append(i)

df = pd.read_json("./data/data_to_plot.json")

le = preprocessing.LabelEncoder()
le.fit(df["sequenceNumber"])
df["sequenceNumber"] = le.transform(df["sequenceNumber"])

le.fit(df["semester"])
df["semester"] = le.transform(df["semester"])

plots = [
    {
        "name": "# Offerings",
        "filename": "plots/num_offerings.png"
    },
    {
        "name": "# prereqs",
        "filename": "plots/num_prereqs.png"
    },
    {
        "name": "# prereqs prev sem",
        "filename": "plots/num_prereqs_prev_sem.png"
    },
    {
        "name": "# students in prereqs",
        "filename": "plots/num_students_in_prereqs.png"
    },
    {
        "name": "semester",
        "filename": "plots/semester.png"
    },
    {
        "name": "# Y1",
        "filename": "plots/num_y1.png"
    },
    {
        "name": "# Y2",
        "filename": "plots/num_y2.png"
    },
    {
        "name": "# Y3",
        "filename": "plots/num_y3.png"
    },
    {
        "name": "# Y4",
        "filename": "plots/num_y4.png"
    },
    {
        "name": "# Y5+",
        "filename": "plots/num_y5+.png"
    }
]

for plot in plots:
    fig, axes = plt.subplots(2, 1)
    plt.subplots_adjust(top=0.9, bottom=0.1, hspace=0.2)

    ndf = df.groupby(["capacity"])[plot["name"]].mean()
    ndf.plot(style=".", color="blue", ylabel=plot["name"], xticks=xAxisTicks, ax=axes[0], figsize=(12, 8))
    df.hist(column=plot["name"], bins=10, ax=axes[1], figsize=(12, 8))
    # df.plot(kind="scatter", x="capacity", y=plot["name"], ylabel=plot["name"], color="blue")
    plt.savefig(plot["filename"])
    plt.clf()
