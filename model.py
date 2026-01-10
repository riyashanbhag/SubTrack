import pandas as pd
from datetime import datetime

def analyze_subscriptions(csv_path):
    df = pd.read_csv(csv_path)
    
    today = pd.to_datetime(datetime.today().date())
    df["next_billing"] = pd.to_datetime(df["next_billing"])

    # Days left until billing
    df["days_left"] = (df["next_billing"] - today).dt.days

    # Status logic (calm, management-focused)
    def status(row):
        if row["days_left"] <= 5 and row["usage_feel"] == "low":
            return "needs-attention"
        elif row["days_left"] <= 10:
            return "review"
        else:
            return "on-track"

    df["status"] = df.apply(status, axis=1)

    # Notes for clarity
    def note(row):
        if row["status"] == "needs-attention":
            return "Billing soon with low recent usage"
        elif row["status"] == "review":
            return "Billing approaching"
        else:
            return "No action needed"

    df["note"] = df.apply(note, axis=1)

    # Top insights
    total_spend = round(df["cost"].sum(), 2)

    next_billing_date = (
        df[df["days_left"] >= 0]
        .sort_values("days_left")
        .iloc[0]["next_billing"]
        .strftime("%d %b %Y")
    )

    needs_attention_count = (df["status"] == "needs-attention").sum()
    low_usage_count = (df["usage_feel"] == "low").sum()

    return (
        df,
        total_spend,
        next_billing_date,
        needs_attention_count,
        low_usage_count
    )
