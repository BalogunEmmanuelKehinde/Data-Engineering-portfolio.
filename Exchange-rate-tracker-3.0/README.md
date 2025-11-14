📊 Exchange Rate Tracker 3.0 — Automated ETL Pipeline

Third iteration with resume-after-downtime system

Project Overview
This project collects live foreign-exchange (FX) data from an API, stores it in MySQL, calculates percentage changes, and visualizes the trends in Power BI.

Version 3.0 introduces major reliability improvements:
Automatic hourly data collection
Resume-from-last-update logic (no data gaps even if laptop or a system goes offline)
Percent change calculations
Power BI dashboard (in progress)
Multi-currency tracking: NGN, USD, EUR, GBP

Tech Stack

Tool	Purpose
Python	Requests, scheduling, ETL logic
MySQL	Database + table storage
Power BI	Visualization
ExchangeRate-API	Live exchange rate data

📂 Project Files
File	Description

exchange3_0_etl.py	Main ETL script (fetch, transform, load, resume logic)
exchange3_0_etl.sql	Database and table schema
exchange3_dashboard.png	(Upcoming) Power BI dashboard

How the ETL Pipeline Works
1. Extract
Python pulls the latest exchange rates using the API endpoint
Base currency: USD
Tracked targets: NGN, EUR, GBP
2. Transform
Convert timestamp
Retrieve previous rate from MySQL
Calculate % change using:
((new_rate - old_rate) / old_rate) * 100
3. Load
Insert into exchange3_rates table
Includes: base_currency, target_currency, rate, date_collected, percent_change
4. Reliability Feature
If your laptop goes off or internet disconnects:
Script detects last saved timestamp
Automatically fills in the missed hours
No gaps in the dataset (this is what makes v3.0 superior)

Database Schema
CREATE TABLE exchange3_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    base_currency VARCHAR(10),
    target_currency VARCHAR(10),
    rate DECIMAL(10,4),
    percent_change DECIMAL(10,4),
    date_collected DATETIME
);

How to Run the Project
1. Create the database
CREATE DATABASE exchange3_0_data
2. Create table;
Import the exchange3_0_etl.sql file into MySQL.
3. Install dependencies
pip install requests schedule mysql-connector-python
4. Run the ETL script
python exchange3_0_etl.py
5. Leave it running
It updates every 1 hour and auto-recovers if you go offline.

Dashboard (coming soon)
Once enough data accumulates, the Power BI dashboard will show:
FX trend over time
Volatility
Hourly & daily % change
Compare NGN, EUR, GBP performance against USD

🏷 About Version 3.0

This is the third iteration of my exchange-rate ETL project.
Each version improves on the previous:

1.0 – Basic pipeline

2.0 – Multi-currency + API improvements

3.0 – Reliability, percent change, resume logic, but i noticed a time stamp issue that needs to be thought through

(4.0 (probably) — fix time stamp issue, alerts, maybe a notification system (probably))
