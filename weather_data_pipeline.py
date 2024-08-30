import requests
import sqlite3
import time
import schedule
import threading
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkcalendar import DateEntry  # Import DateEntry for date selection

API_KEY = 'dfbcddad699ade211c7cf54a75154cf9'  # Replace with your actual API key
your_city = 'Hong Kong'
API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={your_city}&appid={API_KEY}&units=metric'

# Global variable to store the database path
db_path = 'weather_data.db'

# Task 1: Define a database and table
def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            temperature REAL,
            humidity INTEGER,
            weather TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_weather_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'timestamp': datetime.now(),
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'weather': data['weather'][0]['description'],
            }
            print("Fetched weather data:", weather_data)

            # Data Insertion
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO weather (timestamp, temperature, humidity, weather)
                VALUES (?, ?, ?, ?)
            ''', (weather_data['timestamp'], weather_data['temperature'], weather_data['humidity'], weather_data['weather']))
            conn.commit()
            conn.close()
            print("Data inserted successfully.")
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
    except Exception as e:
        print("Request failed:", e)

def fetch_all_data(start_date=None, end_date=None):
    with sqlite3.connect(db_path) as conn:
        if start_date and end_date:
            query = "SELECT * FROM weather WHERE timestamp BETWEEN ? AND ?"
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        else:
            df = pd.read_sql_query("SELECT * FROM weather", conn)
    print(df)  # Debug: print the DataFrame
    return df

def plot_temperature_trends(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['temperature'], marker='o', linestyle='-', color='b', label='Temperature')
    plt.axhline(y=df['temperature'].max(), color='r', linestyle='--', label='Max Temperature')  # Max temperature line
    plt.title('Temperature Trends Over Time')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()
    plt.legend()
    plt.show()

def plot_humidity_trends(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['humidity'], marker='o', linestyle='-', color='g')
    plt.title('Humidity Trends Over Time')
    plt.xlabel('Date and Time')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()
    plt.show()

def generate_report(start_date, end_date):
    df_filtered = fetch_all_data(start_date=start_date, end_date=end_date)
    if df_filtered.empty:
        print("No data found for the specified date range.")
        return

    avg_temp = df_filtered['temperature'].mean()
    max_temp = df_filtered['temperature'].max()
    min_temp = df_filtered['temperature'].min()
    avg_hum = df_filtered['humidity'].mean()

    print(f"Average Temperature: {avg_temp:.2f} °C")
    print(f"Max Temperature: {max_temp:.2f} °C")
    print(f"Min Temperature: {min_temp:.2f} °C")
    print(f"Average Humidity: {avg_hum:.2f} %")

    plot_temperature_trends(df_filtered)
    plot_humidity_trends(df_filtered)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# GUI Functions
def start_fetching():
    interval = interval_entry.get()
    if interval.isdigit() and int(interval) > 0:
        schedule.every(int(interval)).minutes.do(fetch_weather_data)
        messagebox.showinfo("Scheduler Started", f"Fetching weather data every {interval} minute(s).")
    else:
        messagebox.showwarning("Invalid Input", "Please enter a valid positive integer.")

def stop_fetching():
    schedule.clear()
    messagebox.showinfo("Scheduler Stopped", "Weather data fetching has been stopped.")

def analyze_weather_data():
    df = fetch_all_data()
    if df.empty:
        messagebox.showinfo("No Data", "No weather data available for analysis.")
        return

    avg_temp = df['temperature'].mean()
    max_temp = df['temperature'].max()
    min_temp = df['temperature'].min()
    avg_hum = df['humidity'].mean()

    analysis_results = (
        f"Average Temperature: {avg_temp:.2f} °C\n"
        f"Max Temperature: {max_temp:.2f} °C\n"
        f"Min Temperature: {min_temp:.2f} °C\n"
        f"Average Humidity: {avg_hum:.2f} %"
    )
    messagebox.showinfo("Weather Data Analysis", analysis_results)

def generate_report_gui():
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    generate_report(start_date, end_date)

def create_gui():
    root = tk.Tk()
    root.title("Weather Data Interface")

    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Interval Entry for Scheduler
    tk.Label(frame, text="Enter interval (minutes):").pack(pady=5)
    global interval_entry
    interval_entry = tk.Entry(frame)
    interval_entry.pack(pady=5)

    start_button = tk.Button(frame, text="Start Fetching", command=start_fetching)
    start_button.pack(pady=10)

    stop_button = tk.Button(frame, text="Stop Fetching", command=stop_fetching)
    stop_button.pack(pady=10)

    analyze_button = tk.Button(frame, text="Analyze Weather Data", command=analyze_weather_data)
    analyze_button.pack(pady=10)

    plot_button = tk.Button(frame, text="Plot Temperature Change", command=lambda: plot_temperature_trends(fetch_all_data()))
    plot_button.pack(pady=10)

    # Date selection for report generation
    tk.Label(frame, text="Select Start Date:").pack(pady=5)
    global start_date_entry
    start_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.pack(pady=5)

    tk.Label(frame, text="Select End Date:").pack(pady=5)
    global end_date_entry
    end_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    end_date_entry.pack(pady=5)

    report_button = tk.Button(frame, text="Generate Report", command=generate_report_gui)
    report_button.pack(pady=10)

    root.mainloop()

def main():
    create_table()
    fetch_weather_data()

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True  # Daemonize thread
    scheduler_thread.start()

    # Create GUI
    create_gui()

if __name__ == "__main__":
    main()