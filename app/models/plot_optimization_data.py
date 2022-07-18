import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

df = pd.read_csv("./data/optimization_results.csv")

plots = [
	{	
		"name":"Gamma",
		"filename":"plots/gamma.png"
	},
	{	
		"name":"LearningRate",
		"filename":"plots/learning_rate.png"
	},
	{	
		"name":"MaxDepth",
		"filename":"plots/max_depth.png"
	},
    {	
		"name":"RegAlpha",
		"filename":"plots/reg_alpha.png"
	}
]

for plot in plots:
	ndf = df.groupby(plot["name"])["TestMAE"].mean()
	ndf.plot(style='.', color='blue', ylabel="TestMAE")
	plt.savefig(plot["filename"])
	plt.clf()