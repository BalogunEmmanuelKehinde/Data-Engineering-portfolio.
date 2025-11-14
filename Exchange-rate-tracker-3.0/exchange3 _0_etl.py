import requests
import mysql.connector
from datetime import datetime, timedelta
import schedule
import time
from decimal import Decimal


API_KEY = ""# ✅ API key (replace with your own)

# ✅ Currencies to track
CURRENCIES = ['NGN', 'EUR', 'GBP', 'CAD', 'JPY', 'ZAR', 'AUD', 'CNY']

# ✅ Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="",
        user="" , 
        password="" #mysql password,
        database="" #database name on mysql
    )

# ✅ Fetch data from the API
def fetch_exchange_rates():
    url = f""       #url from the web
    response = requests.get(url)
    return response.json()

# ✅ Insert or update rates in MySQL
def insert_rates():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        data = fetch_exchange_rates()
        base_currency = data["base_code"]
        rates = data["conversion_rates"]
        current_time = datetime.now()

        for currency in CURRENCIES:
            if currency in rates:
                rate = Decimal(str(rates[currency]))

                # Check the last recorded rate
                cursor.execute("""
                    SELECT rate FROM exchange3_rates
                    WHERE target_currency = %s
                    ORDER BY date_collected DESC
                    LIMIT 1
                """, (currency,))
                last_rate = cursor.fetchone()

                percent_change = None
                if last_rate:
                    last_rate = Decimal(str(last_rate[0]))
                    if last_rate != 0:
                        percent_change = ((rate - last_rate) / last_rate) * 100

                # Insert new rate
                cursor.execute("""
                    INSERT INTO exchange3_rates (base_currency, target_currency, rate, percent_change, date_collected)
                    VALUES (%s, %s, %s, %s, %s)
                """, (base_currency, currency, rate, percent_change, current_time))

        conn.commit()
        print(f"✅ Data inserted successfully at {current_time}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if conn.is_connected():
            conn.close()

# ✅ Smart Resume Function
def resume_from_last_update():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date_collected) FROM exchange3_rates")
        last_time = cursor.fetchone()[0]

        if last_time:
            print(f"📅 Last update was at {last_time}")
            now = datetime.now()
            diff_hours = int((now - last_time).total_seconds() // 3600)
            if diff_hours > 1:
                print(f"⏳ Missing {diff_hours} hours — fetching retroactive data...")
                for _ in range(diff_hours):
                    insert_rates()
                    time.sleep(1)
        else:
            print("🚀 First time setup, inserting initial data...")
            insert_rates()

    except Exception as e:
        print(f"❌ Error resuming updates: {e}")

    finally:
        if conn.is_connected():
            conn.close()

# ✅ Schedule hourly updates
resume_from_last_update()
schedule.every(1).hours.do(insert_rates)

print("🔁 Exchange Rate Tracker 3.0 running — updates every 1 hour")

while True:
    schedule.run_pending()
    time.sleep(60)
    

    #to run in terminal type - python 'database name' etl.py