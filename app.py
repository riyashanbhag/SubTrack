from flask import Flask, render_template, request, redirect, send_file
from model import analyze_subscriptions, predict_spend
import csv
import os

app = Flask(__name__)

CSV_PATH = "data/subscriptions.csv"

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Ensure CSV file exists
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "cost", "category", "usage_feel", "next_billing"])


@app.route("/")
def index():

    df, total_spend, next_billing, needs_attention, low_usage, suggestions, monthly_spend, category_spend = analyze_subscriptions(CSV_PATH)

    prediction = predict_spend(df)

    return render_template(
        "index.html",
        subscriptions=df.to_dict(orient="records"),
        total_spend=total_spend,
        next_billing=next_billing,
        needs_attention=needs_attention,
        low_usage=low_usage,
        suggestions=suggestions,
        monthly_spend=monthly_spend,
        prediction=prediction,
        category_spend=category_spend
    )


@app.route("/add", methods=["POST"])
def add_subscription():

    name = request.form["name"]
    cost = float(request.form["cost"])
    category = request.form["category"]
    usage_feel = request.form["usage_feel"]
    next_billing = request.form["next_billing"]

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, cost, category, usage_feel, next_billing])

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete_subscription():

    name = request.form["name"]

    with open(CSV_PATH, "r") as f:
        rows = list(csv.reader(f))

    header = rows[0]
    new_rows = [header]

    for row in rows[1:]:
        if row[0] != name:
            new_rows.append(row)

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/")


@app.route("/download")
def download():
    return send_file(CSV_PATH, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)