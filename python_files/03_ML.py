# HW 4
# Brenton Wilder
import sys

import statsmodels.api
from plotly import express as px
from sklearn import datasets
import numpy as np

def main():
    breast_cancer = datasets.load_breast_cancer()
    X = breast_cancer.data
    y = breast_cancer.target

    for idx, column in enumerate(X.T):
        feature_name = breast_cancer.feature_names[idx]
        predictor = statsmodels.api.add_constant(column)
        # Continuous response, y
        if y.dtype == np.number:
            linear_regression_model = statsmodels.api.OLS(y, predictor)
            linear_regression_model_fitted = linear_regression_model.fit()
            print(f"Variable: {feature_name}")
            print(linear_regression_model_fitted.summary())
            # Get the stats
            t_value = round(linear_regression_model_fitted.tvalues[1], 6)
            p_value = "{:.6e}".format(linear_regression_model_fitted.pvalues[1])
            # Plot the figure
            fig = px.scatter(x=column, y=y, trendline="ols")
            fig.update_layout(
            title=f"Variable: {feature_name}: (t-value={t_value}) (p-value={p_value})",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y")
            fig.show()
        else: 
            # Logistic regression for boolean response, y
            print("working on bool response")
    
    return
 
 
if __name__ == "__main__":
    sys.exit(main())
