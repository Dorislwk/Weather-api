# Weather Data Fetching and Analysis

## 1. Introduction 🎯
The weather pipeline is available for fetching real-time weather data and fostering analysis about Hong Kong, ultimately building a foundation for daily personal decisions regarding commuting and predicting weather trends for professional use.

## 2. Table of Content
- Core Features
- Project Structure
- Files and Usage
- Getting Started
- GUI Overview
- Acknowledgments

## 3. Core Features
1. API integration
2. Schedler
3. User interface for data analysis
4. Database setup


## 4. Project Structure
```
│
└── weather_data_pipeline.py 🚀
```

## 5. Files and Usage 🔍
- weather_data_pipeline.py: Integrates an API for real-time weather data fetching and analysis general statistics, visualizes the results, provides a GUI for user interaction, and connects to an SQLite database for data storage.


## 6. Getting Started 🧰
1. Setup: Ensure you have the required libraries installed. You can install them using pip:

```
pip install -r requirements.txt
```

2. Create a connection: You must connect to the database before using it.

```
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
```


3. Data Processing and Analysis: Execute the weather_data_pipeline.py file to start the fenching and analysis:

```
weather_data_pipeline.py
```


## 7. GUI Overview
![image](https://github.com/Dorislwk/Weather_api/blob/main/photo/GUI%20for%20weather%20pipeline.png)

## 8. Acknowledgments 📊
- OpenWeather API
- URL: https://openweathermap.org/api 