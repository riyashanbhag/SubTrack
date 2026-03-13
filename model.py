import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np


def analyze_subscriptions(csv_path):

    df = pd.read_csv(csv_path)

    # If CSV has no rows
    if df.empty:
        return df, 0, "No upcoming bills", 0, 0, [], {}, {}

    today = pd.to_datetime(datetime.today().date())

    df["next_billing"] = pd.to_datetime(df["next_billing"])

    df["days_left"] = (df["next_billing"] - today).dt.days


    # STATUS LOGIC
    def status(row):
        if row["days_left"] <= 5 and row["usage_feel"] == "low":
            return "needs-attention"
        elif row["days_left"] <= 10:
            return "review"
        else:
            return "on-track"

    df["status"] = df.apply(status, axis=1)


    # NOTE LOGIC
    def note(row):
        if row["status"] == "needs-attention":
            return "Billing soon with low usage"
        elif row["status"] == "review":
            return "Billing approaching"
        else:
            return "No action needed"

    df["note"] = df.apply(note, axis=1)


    # TOTAL SPEND
    total_spend = round(df["cost"].sum(), 2)


    # NEXT BILLING DATE
    upcoming = df[df["days_left"] >= 0].sort_values("days_left")

    if len(upcoming) > 0:
        next_billing = upcoming.iloc[0]["next_billing"].strftime("%d %b %Y")
    else:
        next_billing = "No upcoming bills"


    # COUNTS
    needs_attention = (df["status"] == "needs-attention").sum()

    low_usage = (df["usage_feel"] == "low").sum()


    # SMART SUGGESTIONS
    suggestions = []

    for _, row in df.iterrows():
        if row["usage_feel"] == "low":
            suggestions.append(row["name"])


    # MONTHLY SPEND
    df["month"] = df["next_billing"].dt.month

    monthly_spend = df.groupby("month")["cost"].sum().to_dict()


    # CATEGORY SPEND
    if "category" in df.columns:
        category_spend = df.groupby("category")["cost"].sum().to_dict()
    else:
        category_spend = {}


    return (
        df,
        total_spend,
        next_billing,
        needs_attention,
        low_usage,
        suggestions,
        monthly_spend,
        category_spend
    )


def predict_spend(df):

    # Not enough data
    if len(df) < 2:
        return round(df["cost"].sum(), 2)

    df["month"] = df["next_billing"].dt.month

    monthly = df.groupby("month")["cost"].sum().reset_index()

    X = monthly["month"].values.reshape(-1, 1)
    y = monthly["cost"].values

    model = LinearRegression()
    model.fit(X, y)

    next_month = np.array([[monthly["month"].max() + 1]])

    prediction = model.predict(next_month)

    return round(prediction[0], 2)