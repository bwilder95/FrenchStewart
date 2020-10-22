# Midterm
# Brenton Wilder
# October 23, 2020

# Import libraries
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS
from plotly import express as px
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


"""
Datsets this code works with:
load_boston() , yes
load_iris() , yes
load_diabetes(), yes
load_digits() , NO
load_linnerud() , NO
load_breast_cancer() , yes
load wine() , yes
"""


# Define my main
def main():
    # Input your dataset here *******************
    dataset = load_iris()
    data = dataset.data
    features = dataset.feature_names
    df = pd.DataFrame(data, columns=features)
    # print(df.shape)
    # print(features)

    # Plot Correlation metrics
    df_all = df.iloc[:, :]
    cor_mat = df_all.corr(method="pearson")
    sns.set(font_scale=0.6)
    sns.heatmap(cor_mat, annot=True)
    plt.show()

    # Loop through df cor_mat to get each metric
    df_metric = pd.DataFrame()
    for rows in cor_mat:
        df_metric = df_metric.append(cor_mat[rows])
    # print(df_metric.head())

    # Save this metric table to html
    html = df_metric.to_html()
    txtfile = open("pearson.html", "w")
    txtfile.write(html)
    txtfile.close()

    # Combined relationship plot
    # Run through all possible cases (Brute Force)
    # Setting 2 as the maximum number of features for time.
    # Cat response
    X = dataset.data
    y = dataset.target
    if y.dtype != np.number and X.dtype == np.number:
        knn = KNeighborsClassifier(n_neighbors=3)
        efs1 = EFS(
            knn,
            min_features=1,
            max_features=2,
            scoring="accuracy",
            print_progress=True,
            cv=5,
        )

        efs1 = efs1.fit(X, y)
        bf = pd.DataFrame.from_dict(efs1.get_metric_dict()).T
        bf.sort_values("avg_score", inplace=True, ascending=False)
        print(bf.head())
        html2 = bf.to_html()
        txtfile = open("BruteForceRankings_cat.html", "w")
        txtfile.write(html2)
        txtfile.close()

        metric_dict = efs1.get_metric_dict()
        k_feat = sorted(metric_dict.keys())
        avg = [metric_dict[k]["avg_score"] for k in k_feat]
        upper, lower = [], []
        for k in k_feat:
            upper.append(metric_dict[k]["avg_score"] + metric_dict[k]["std_dev"])
            lower.append(metric_dict[k]["avg_score"] - metric_dict[k]["std_dev"])

        plt.fill_between(k_feat, upper, lower, alpha=0.2, color="blue", lw=1)
        plt.plot(k_feat, avg, color="blue", marker="o")
        plt.ylabel("Accuracy +/- Standard Deviation")
        plt.xlabel("Number of Features")
        plt.xticks(
            k_feat, [str(metric_dict[k]["feature_names"]) for k in k_feat], rotation=90
        )
        plt.show()

    # Cont response. Setting max=2 for sake of time.
    else:
        lr = LinearRegression()
        efs = EFS(
            lr, min_features=1, max_features=2, scoring="neg_mean_squared_error", cv=10
        )

        efs.fit(X, y)
        bf = pd.DataFrame.from_dict(efs.get_metric_dict()).T
        bf.sort_values("avg_score", inplace=True, ascending=False)
        print(bf.head())
        html2 = bf.to_html()
        txtfile = open("BruteForceRankings_cont.html", "w")
        txtfile.write(html2)
        txtfile.close()

        metric_dict = efs.get_metric_dict()
        k_feat = sorted(metric_dict.keys())
        avg = [metric_dict[k]["avg_score"] for k in k_feat]
        upper, lower = [], []
        for k in k_feat:
            upper.append(metric_dict[k]["avg_score"] + metric_dict[k]["std_dev"])
            lower.append(metric_dict[k]["avg_score"] - metric_dict[k]["std_dev"])

        plt.fill_between(k_feat, upper, lower, alpha=0.2, color="red", lw=1)
        plt.plot(k_feat, avg, color="red", marker="o")
        plt.ylabel("Accuracy +/- Standard Deviation")
        plt.xlabel("Number of Features")
        plt.xticks(
            k_feat, [str(metric_dict[k]["feature_names"]) for k in k_feat], rotation=90
        )
        plt.show()

    # Plot histograms for different features
    for idx, column in enumerate(X.T):
        feature_name = dataset.feature_names[idx]
        predictor = statsmodels.api.add_constant(column)

        # Continuous
        if y.dtype == np.number:
            linear_regression_model = statsmodels.api.OLS(y, predictor)
            linear_regression_model_fitted = linear_regression_model.fit()
            print(f"Variable: {feature_name}")
            print(linear_regression_model_fitted.summary())
            # Get the stats
            t_value = round(linear_regression_model_fitted.tvalues[1], 6)
            p_value = "{:.6e}".format(linear_regression_model_fitted.pvalues[1])
            # Plot the figure to a local html file
            fig = px.scatter(x=column, y=y, trendline="ols")
            fig2 = px.histogram(x=column, nbins=20)
            # This is not working, giving NaN
            _, bins = np.histogram(column, bins=20)
            bin_means = pd.Series(column).groupby(pd.cut(column, bins)).mean()
            Sumallll = sum(column)
            pop_avg = Sumallll / all(column)
            Diff = 1 / 20 * sum(bin_means - pop_avg) ** 2
            fig.update_layout(
                title=f"Variable:{feature_name}:(t-value={t_value})(p-value={p_value})",
                xaxis_title=f"Variable: {feature_name}",
                yaxis_title="y",
            )
            fig2.update_layout(
                title=f"Variable:{feature_name}:Mean difference = {Diff}",
                xaxis_title=f"Variable: {feature_name}",
                yaxis_title="count",
            )
            with open("./MeanOfResponse_cont.html", "a") as f:
                f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
                f.write(fig2.to_html(full_html=False, include_plotlyjs="cdn"))
        else:
            # Categorical response
            logistic_regression_model = LogisticRegression(random_state=1234).fit(
                predictor, y
            )
            print(f"Variable: {feature_name} Fit Score")
            print(logistic_regression_model.score(predictor, y))
            score = logistic_regression_model.score(predictor, y)
            # Plot the Figure to a local html file
            fig = px.violin(x=y, y=column)
            fig.update_layout(
                title=f"Variable:{feature_name},Logistic Regression Fit Score={score}",
                xaxis_title=f"Variable: {feature_name}",
                yaxis_title="y",
            )
            with open("./MeanOfResponse_cat.html", "a") as f:
                f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))


if __name__ == "__main__":
    sys.exit(main())
