from flask import Flask, render_template, request, redirect
from model import analyze_subscriptions
import csv

app = Flask(__name__)
CSV_PATH = "data/subscriptions.csv"

@app.route("/")
def index():
    df, total_spend, next_billing, needs_attention, low_usage = analyze_subscriptions(CSV_PATH)

    return render_template(
        "index.html",
        subscriptions=df.to_dict(orient="records"),
        total_spend=total_spend,
        next_billing=next_billing,
        needs_attention=needs_attention,
        low_usage=low_usage
    )

@app.route("/add", methods=["POST"])
def add_subscription():
    data = [
        request.form["name"],
        float(request.form["cost"]),
        request.form["next_billing"],
        request.form["usage_feel"]
    ]

    with open(CSV_PATH, "a", newline="") as f:
        csv.writer(f).writerow(data)

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_subscription():
    name = request.form["name"]

    rows = []
    with open(CSV_PATH, "r") as f:
        rows = list(csv.reader(f))

    header = rows[0]
    updated_rows = [header]

    for row in rows[1:]:
        if row[0] != name:
            updated_rows.append(row)

    with open(CSV_PATH, "w", newline="") as f:
        csv.writer(f).writerows(updated_rows)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
