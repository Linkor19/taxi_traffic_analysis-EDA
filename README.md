# NYC Taxi Trip and Weather Data Analysis

An exploratory data analysis (EDA) project investigating the relationship between New York City taxi trip patterns, weather conditions, and urban geography. This project combines **Python** for data processing/visualization and **SQL** for complex data aggregation.

## 📌 Project Overview
The goal of this project is to analyze how environmental factors (temperature, precipitation, snow) and temporal factors (seasons, hours, holidays) affect taxi demand, trip duration, and distance in NYC.

## 🛠️ Tech Stack
* **Python:** `pandas`, `numpy`, `matplotlib`, `seaborn`
* **Geospatial Analysis:** `geopandas`, `shapely`
* **SQL:** Data analysis via Google Cloud DataLab / DuckDB

## 📂 Data Sources
* `train.csv`: Primary dataset containing taxi trip details (pickup/dropoff times, coordinates).
* `weather.csv`: Daily weather metrics for NYC (precipitation, snow, temperature).
* `2020_Neighborhood_Tabulation_Areas__NTAs_.csv`: Geospatial boundaries used to map coordinates to specific neighborhoods.

## 🚀 Key Features
### 1. Data Cleaning & Engineering
* **Weather Normalization:** Handled "Trace" (T) precipitation values by converting them to a numeric constant ($0.05$).
* **Distance Calculation:** Implemented the Haversine formula to calculate the geographic distance (km) between pickup and dropoff points.
* **Spatial Joins:** Used `geopandas` to perform point-in-polygon joins, assigning each trip to a specific NYC Borough and Neighborhood (NTA).

### 2. Statistical Analysis & Visualizations
* **Correlation Heatmaps:** Analyzing the relationship between weather variables and trip duration.
* **Temporal Trends:** Visualizing peak hours and seasonal demand fluctuations.
* **Geospatial Insights:** Identifying the most popular pickup and dropoff locations across the five boroughs.
* **Vendor Performance:** Comparing trip distributions between different taxi vendors.

### 3. SQL Analytics
The analysis includes high-performance SQL queries for:
* Identifying the busiest months and dates.
* Analyzing trip duration trends on holidays vs. weekdays.
* Aggregating seasonal weather averages (rolling means and group-bys).

---

## 💻 How to Run the SQL Queries
The SQL scripts in this project were originally executed in **Google Cloud DataLab**. 

To run these queries locally or in other environments:
1.  **Direct CSV Querying:** Use a tool like **DuckDB** or **DBeaver** (with the CSV driver) that allows you to run SQL directly against `.csv` files.
    * *Note:* Ensure the file paths in the `FROM` clauses (e.g., `'taxi_data/data/train.csv'`) match your local directory structure.
2.  **Database Connection:** Alternatively, you can import the CSV files into a database (PostgreSQL/SQLite) and update the table names in the queries accordingly.

## 📊 Sample Visualizations
The project generates several key plots:
* Trip Duration vs. Temperature.
* Average Passenger Count by Precipitation Levels.
* Top 10 Districts by Seasonally Adjusted Trip Counts.
* Vendor market share (Pie Charts).

---
