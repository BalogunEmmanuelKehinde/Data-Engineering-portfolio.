📊 Exchange Rate Tracker 3.0  
A real-time automated exchange rate tracker built with Python,MySQL,and Power-BI.

This is the third iteration (3.0) of my exchange-rate ETL project.  
Version 3.0 improves reliability by resuming data collection even after the system goes offline, ensuring zero data gaps.

Project Overview
The goal of this project is to collect live foreign-exchange rates every hour, store them in MySQL, calculate the percentage changes, and visualize long-term currency trends in Power BI.

This version includes:
Automatic hourly data collection  
Resume-from-last-update logic (so no missing data from when the code first ran))  
Percentage change calculations  
Power BI dashboard(i'll get to it)

Tech Stack
Python – requests, schedule, mysql-connector  
MySQL – database & table design  
Power BI – visualization  
REST API – ExchangeRate-API
