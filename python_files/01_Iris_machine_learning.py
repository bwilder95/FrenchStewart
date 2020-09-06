# Iris Machine Learning Assignment
# Brenton Wilder
# September 5th, 2020

# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read iris data and add appropriate column headers
Iris = pd.read_csv("data/iris.data", header=None)
Iris.columns = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "class",
]

# Calculate basic statistics of the dataset
print(Iris.describe(include="all"))

# Figure 1 - Violin plot comparing petal length (cm)
plt.figure()
bx = sns.violinplot(x="class", y="petal length (cm)", data=Iris)

# Figure 2 - Box plots of measurements
plt.figure()
ax = sns.boxplot(data=Iris)
medians = Iris.median().values
nobs = Iris.count()
nobs = [str(x) for x in nobs.tolist()]
nobs = ["n: " + i for i in nobs]
pos = range(len(nobs))
for tick, label in zip(pos, ax.get_xticklabels()):
    ax.text(
        pos[tick],
        medians[tick] + 0.03,
        nobs[tick],
        horizontalalignment="center",
        size="x-small",
        color="w",
        weight="semibold",
    )

# Figure 3 - Multiple linear regression
dx = sns.lmplot(
    x="sepal length (cm)", y="sepal width (cm)", hue="class", height=5, data=Iris
)

# Figure 4 - Scatterplot matrix
sns.set(style="ticks")
sns.pairplot(Iris, hue="class")

# Figure 5 - Scatterplot with categorical and numerical semantics
plt.figure()
sns.set(style="whitegrid")
cx = sns.scatterplot(
    x="petal width (cm)",
    y="petal length (cm)",
    hue="class",
    size="sepal length (cm)",
    palette="ch:r=-.2,d=.3_r",
    sizes=(20, 100),
    linewidth=0,
    data=Iris,
)
plt.show()
