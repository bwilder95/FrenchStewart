# Midterm
# Brenton Wilder
# October 23, 2020

# Instructions
"""
Given a pandas dataframe
    Contains both a response and predictors
    Assume you could have either have a boolean or continuous response

Split dataset predictors between categoricals and continuous
    Assume only nominal categoricals (no ordinals)

Calculate correlation metrics between all:
    Continuous / Continuous pairs
    Continuous / Categorical pairs
    Categorical / Categorical pairs
    Put values in tables ordered DESC by correlation metric
    Put links to the original variable plots done in HW #4
    Generate correlation matricies for the above 3

Calculate "Brute-Force" variable combinations between all:
    Continuous / Continuous pairs
    Continuous / Categorical pairs
    Categorical / Categorical pairs
    Calculate weighted and unweighted "difference with mean of response" metric
    Put values in tables ordered DESC by the "weighted" ranking metric
    For each of the combinations generate the necessary plots to help see the relationships
    "Link" to these plots from the table (html, excel)

Final output
3 Correlation tables (With links to individual plots done in HW#4)
3 Correlation Matricies
3 "Brute Force" tables, with links to plots showing combined relationship

I'm going to grade this by giving it some random dataset and seeing if it outputs everything
"""

# Import libraries
import sys
import numpy as np
import pandas as pd
import statsmodels.api
from plotly import express as px
from sklearn import datasets, metrics
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS

# Define my main
def main():

    # Input dataset
    breast_cancer = load_breast_cancer()
    data = breast_cancer.data
    features = breast_cancer.feature_names
    df = pd.DataFrame(data, columns = features)
    print(df.shape)
    #print(features)

    # Plot Correlation metrics
    df_all = df.iloc[:,:]
    cor_mat = df_all.corr(method='pearson')
    sns.set(font_scale=0.6) 
    sns.heatmap(cor_mat, annot = True)
    #plt.show()

    # Loop through df cor_mat to get each metric
    df_metric = pd.DataFrame()
    for rows in cor_mat:
        df_metric = df_metric.append(cor_mat[rows])
    print(df_metric.head())

    # Save this metric table to html
    html = df_metric.to_html()
    txtfile = open("pearson.html","w")
    txtfile.write(html)
    txtfile.close()

    X = breast_cancer.data
    y = breast_cancer.target
    knn = KNeighborsClassifier(n_neighbors=3)
    efs1 = EFS(knn, 
           min_features=1,
           max_features=3,
           scoring='accuracy',
           print_progress=True,
           cv=5)
    
    efs1 = efs1.fit(X, y)
    bf = pd.DataFrame.from_dict(efs1.get_metric_dict()).T
    bf.sort_values('avg_score', inplace=True, ascending=False)
    print(bf.head())





if __name__ == "__main__":
    sys.exit(main())