import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def forecast_sales(df):

    monthly = df.groupby("order_date")["revenue"].sum().reset_index()

    monthly["month_num"] = np.arange(len(monthly))

    X = monthly[["month_num"]]

    y = monthly["revenue"]

    model = LinearRegression()

    model.fit(X, y)

    future = np.array(range(len(monthly), len(monthly) + 3)).reshape(-1, 1)

    predictions = model.predict(future)

    return predictions
