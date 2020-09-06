# Iris Machine Learning Assignment
# Brenton Wilder
# September 5th, 2020

# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import tree
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, Normalizer, StandardScaler
from sklearn.svm import SVC

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
print("*" * 80)
print("Statistics")
print("*" * 80)
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

# Analyze and build models using scikit-learn
# Print original dataset
print("*" * 80)
print("Original Dataset")
print("*" * 80)
print(Iris)

# DataFrame to numpy arrays
x = Iris[
    [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]
].values
y = Iris["class"].values

# Use LabelEncoder to make categorical variables numeric
lb_make = LabelEncoder()
y = lb_make.fit_transform(y)
print("*" * 80)
print("LabelEncoder changing flower type to 0,1,or 2")
print("*" * 80)
print(y)

# Normalize "x" (predictors)
normalizer = Normalizer().fit(x)
x_norm = normalizer.transform(x)
print("*" * 80)
print("Normalize data to range 0 to 1")
print("*" * 80)
print(x_norm)

# Random forest classifier
rf = RandomForestClassifier(random_state=1234)
rf.fit(x_norm, y)
prediction = rf.predict(x_norm)
probability = rf.predict_proba(x_norm)
print("*" * 80)
print("Random Forest Model Predictions")
print("*" * 80)
print(f"Probability: {probability}")
print(f"Predictions: {prediction}")

# DecisionTreeClassifer
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_norm, y)
clf_pred = clf.predict(x_norm)
clf_prob = clf.predict_proba(x_norm)
plt.figure()
tree.plot_tree(clf, filled=True)
print("*" * 80)
print("Decision Tree Model Predictions")
print("*" * 80)
print(f"Probability: {clf_prob}")
print(f"Predictions: {clf_pred}")

# Creating pipeline for test set with C-Support Vector Classification
x_norm, y = make_classification(random_state=0)
x_train, x_test, y_train, y_test = train_test_split(x_norm, y, random_state=0)
pipe = Pipeline([("scaler", StandardScaler()), ("svc", SVC())])
pipe.fit(x_train, y_train)
print("*" * 80)
print("Pipeline prediction score using SVC")
print("*" * 80)
print(pipe.score(x_test, y_test))

# Plot all figures
plt.show()
