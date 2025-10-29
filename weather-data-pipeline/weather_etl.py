import requests
import mysql.connector
import schedule
import time
from datetime import datetime

# Your OpenWeather API key
API_KEY = "YOUR_API_KEY"

# Cities to track
CITIES = ["Lagos", "Abuja", "Kwara", "Oyo"]

def fetch_and_store_weather():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YOUR_MYSQL_PASSWORD',   # replace with your real password
            database='live_data'
        )
        cursor = conn.cursor()

        for city in CITIES:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Insert data into MySQL
                cursor.execute("""
                    INSERT INTO weather (city, temperature, humidity, description, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (city, temp, humidity, description, timestamp))

                print(f"✅ Inserted weather for {city}: {temp}°C, {humidity}%, {description}")
            else:
                print(f"❌ Failed to fetch weather for {city}: {data}")

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# Schedule: fetch every 30 minutes
schedule.every(30).minutes.do(fetch_and_store_weather)

print("🚀 Weather ETL started... Collecting data every 30 minutes.")
fetch_and_store_weather()  # Run once immediately

while True:
    schedule.run_pending()
    time.sleep(1)