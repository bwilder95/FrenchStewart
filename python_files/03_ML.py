# HW 4
# Brenton Wilder
# Estimated run time is 0:00:04.021005 seconds
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.api
from plotly import express as px
from sklearn import datasets, metrics
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def main():
    start_t = datetime.now()
    # Input dataset
    dataset = datasets.load_diabetes()
    X = dataset.data
    y = dataset.target

    for idx, column in enumerate(X.T):
        feature_name = dataset.feature_names[idx]
        predictor = statsmodels.api.add_constant(column)

        # Continuous predictor, X, and continuous response, y
        if y.dtype == np.number and X.dtype == np.number:
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
            with open("./p_graph.html", "a") as f:
                f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
                f.write(fig2.to_html(full_html=False, include_plotlyjs="cdn"))

        # Categorical predictor, X, and continuous response, y
        elif y.dtype == np.number and X.dtype != np.number:
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
            with open("./p_graph.html", "a") as f:
                f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))

        # Continuous predictor, X, and categorical response, y
        elif y.dtype != np.number and X.dtype == np.number:
            logistic_regression_model = LogisticRegression(random_state=1234).fit(
                predictor, y
            )
            print(f"Variable: {feature_name} Fit Score")
            print(logistic_regression_model.score(predictor, y))
            score = logistic_regression_model.score(predictor, y)
            # Plot the Figure to a local html file
            fig = px.violin(x=y, y=column)
            fig.update_layout(
                title=f"Variable: {feature_name},Logistic Regression Fit Score={score}",
                xaxis_title=f"Variable: {feature_name}",
                yaxis_title="y",
            )
            with open("./p_graph.html", "a") as f:
                f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))

        else:
            # Categorical response, X, categorical response, y
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
            with open("./p_graph.html", "a") as f:
                f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))

    # Continuous predictor, X, and continuous response, y
    if y.dtype == np.number and X.dtype == np.number:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        regressor = RandomForestRegressor(n_estimators=200, random_state=0)
        regressor.fit(X_train, y_train)
        y_pred = regressor.predict(X_test)
        print("******Random forest regression performance*******")
        print("Mean Absolute Error:", metrics.mean_absolute_error(y_test, y_pred))
        print("Mean Squared Error:", metrics.mean_squared_error(y_test, y_pred))
        print(
            "Root Mean Squared Error:",
            np.sqrt(metrics.mean_squared_error(y_test, y_pred)),
        )
        importances = regressor.feature_importances_
        indices = np.argsort(importances)[::-1]
        print("*****Feature ranking:*****")
        for f in range(X.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Categorical predictor, X, and continuous response, y
    elif y.dtype == np.number and X.dtype != np.number:
        rf = RandomForestClassifier(max_depth=2, random_state=0)
        rf.fit(X, y)
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        print("*****Feature ranking:*****")
        for f in range(X.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Continuous predictor, X, and categorical response, y
    elif y.dtype != np.number and X.dtype == np.number:
        rf = RandomForestClassifier(max_depth=2, random_state=0)
        rf.fit(X, y)
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        print("*****Feature ranking:*****")
        for f in range(X.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    else:
        # Categorical response, X, categorical response, y
        rf = RandomForestClassifier(max_depth=2, random_state=0)
        rf.fit(X, y)
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        print("*****Feature ranking:*****")
        for f in range(X.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    print(f" {(datetime.now() - start_t)} seconds")


if __name__ == "__main__":
    sys.exit(main())
