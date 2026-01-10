<h1>SubTrack – Subscription Tracking & Management System</h1>

<h4>SubTrack is a student-focused web application that helps users keep track of all their subscriptions in one place.
It provides visibility into upcoming billing dates, monthly spending, and subscriptions that may need attention — helping users avoid forgotten auto-renewals.</h4>
 <br>
<h3>Features</h3>

Features

Track next billing dates for all subscriptions
View total monthly spending at a glance
Identify subscriptions that need attention
Usage-based status classification (On Track / Review / Needs Attention)
Delete subscriptions after stopping auto-pay
Graceful handling of empty states without crashes
Clean, responsive, and student-friendly user interface

<h3>🛠️ Tech Stack</h3>

Frontend: HTML, CSS, Jinja2
Backend: Python, Flask
Data Handling: Pandas
Deployment: Render
Server: Gunicorn

🧩 How It Works
Users add subscriptions with:
Name
Monthly cost
Next billing date
Approximate usage level

The system calculates:
Days left until billing
Status based on urgency & usage

Dashboard displays:
Next upcoming billing
Total spend
Low-usage subscriptions

Users can delete subscriptions once auto-pay is stopped.



▶️ Running Locally
git clone https://github.com/riyashanbhag/SubTrack.git
<br>
cd SubTrack
<br>

pip install -r requirements.txt
<br>

python app.py


Then open:
http://127.0.0.1:5000
