import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, shape
import json
from shapely import wkt

pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

train_df = pd.read_csv('taxi_data/data/train.csv')
weather = pd.read_csv('taxi_data/data/weather.csv')

train_df['pickup_datetime'] = pd.to_datetime(train_df['pickup_datetime'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
train_df['id_date'] = train_df['pickup_datetime'].dt.date
weather['date'] = pd.to_datetime(weather['date'], format="%m-%d-%Y", errors='coerce')
weather['id_date'] = weather['date'].dt.date
merge_df = train_df.merge(weather, on='id_date')
merge_df['precipitation_n'] = merge_df['precipitation'].replace('T', 0.05).astype(float)
merge_df['snow fall_n'] = merge_df['snow fall'].replace('T', 0.05).astype(float)
merge_df['snow depth_n'] = merge_df['snow depth'].replace('T', 0.05).astype(float)
merge_df['hour'] = merge_df['pickup_datetime'].dt.hour
merge_df['daily_trip_count'] = merge_df.groupby('date')['id'].transform('count')
pickup_lat_rad = np.radians(merge_df['pickup_latitude'])
pickup_lon_rad = np.radians(merge_df['pickup_longitude'])
dropoff_lat_rad = np.radians(merge_df['dropoff_latitude'])
dropoff_lon_rad = np.radians(merge_df['dropoff_longitude'])
dlat = dropoff_lat_rad - pickup_lat_rad
dlon = dropoff_lon_rad - pickup_lon_rad
a = np.sin(dlat / 2) ** 2 + np.cos(pickup_lat_rad) * np.cos(dropoff_lat_rad) * np.sin(dlon / 2) ** 2
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
R = 6371.0
merge_df['distance_km'] = R * c

boroughs_df = pd.read_csv('taxi_data/2020_Neighborhood_Tabulation_Areas__NTAs_.csv')
boroughs_df['geometry'] = boroughs_df['the_geom'].apply(wkt.loads)
boroughs_gdf = gpd.GeoDataFrame(boroughs_df, geometry='geometry')
merge_df['coordinates_pickupp'] = merge_df.apply(lambda row: Point(row['pickup_longitude'], row['pickup_latitude']),
                                                 axis=1)
merge_df['coordinates_dropofff'] = merge_df.apply(lambda row: Point(row['dropoff_longitude'], row['dropoff_latitude']),
                                                  axis=1)
sample_df = merge_df[:500].copy()
sample_df_pickup = gpd.GeoDataFrame(sample_df, geometry='coordinates_pickupp')
sample_df_dropoff = gpd.GeoDataFrame(sample_df, geometry='coordinates_dropofff')

sample_df_pickup = gpd.sjoin(
    sample_df_pickup,
    boroughs_gdf[['geometry', 'NTAName', 'BoroName']],
    how="left",
    predicate='within'
).rename(columns={'NTAName': 'NATName_p', 'BoroName': 'BoroName_p'})

sample_df_dropoff = gpd.sjoin(
    sample_df_dropoff,
    boroughs_gdf[['geometry', 'NTAName', 'BoroName']],
    how="left",
    predicate='within'
).rename(columns={'NTAName': 'NATName_d', 'BoroName': 'BoroName_d'})
sample_df = sample_df_pickup.join(sample_df_dropoff[['NATName_d', 'BoroName_d']])

# sample_df.to_csv('sample_df.csv')

list_of_int_var = ['snow fall_n', 'precipitation_n', 'average temperature', 'hour', 'trip_duration', 'passenger_count',
                   'daily_trip_count', 'distance_km']
list_for_heat_map = list_of_int_var

map_df = pd.DataFrame()
for var in list_for_heat_map:
    if var in merge_df.columns:
        map_df[var] = merge_df[var]
    else:
        print(f"Column {var} not found in DataFrame.")

correlation_matrix = map_df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.show()

plt.scatter(x='average temperature', y='trip_duration',
            data=merge_df[merge_df['trip_duration'] < 20000])  # corr temp / duration
plt.xlabel('Average Temperature')
plt.ylabel('Trip Duration (min)')
plt.title('Trip Duration vs. Average Temperature')
plt.show()

# plt.scatter(x='average temperature', y='passenger_count', data=df)  # corr temp / passeng (illogical)
# plt.xlabel('Average Temperature')
# plt.ylabel('Passenger Count')
# plt.title('Passenger Count vs. Average Temperature')
# plt.show()

# plt.scatter(x='average temperature', y='distance_km', data=df)  # corr temp / distance (illogical)
# plt.xlabel('Average Temperature')
# plt.ylabel('Distance (km)')
# plt.title('Distance vs. Average Temperature')
# plt.show()

merge_df['precipitation_groups'] = (merge_df['precipitation_n'] * 4).round() / 4  # corr precipit / passeng
pre_gr_pas = merge_df.groupby('precipitation_groups')['passenger_count'].mean()
pre_gr_pas.plot(kind='bar')
plt.xlabel('Precipitation Group')
plt.ylabel('Average Passenger Count')
plt.title('Average Passenger Count by Precipitation Groups (4 levels)')
plt.show()

pre_gr_dur = merge_df.groupby('precipitation_groups')['trip_duration'].mean()  # corr precipit / dur
pre_gr_dur.plot(kind='bar')
plt.xlabel('Precipitation Group')
plt.ylabel('Average Trip Duration (min)')
plt.title('Average Trip Duration by Precipitation Groups (4 levels)')
plt.show()

pre_gr_dis = merge_df.groupby('precipitation_groups')['distance_km'].mean()  # corr precipit / distance
pre_gr_dis.plot(kind='bar')
plt.xlabel('Precipitation Group')
plt.ylabel('Average Distance (km)')
plt.title('Average Distance by Precipitation Groups (4 levels)')
plt.show()

merge_df['precipitation_groups'] = (merge_df['precipitation_n'] * 10).round() / 10  # corr precipit / count
pre_gr_pas = merge_df.groupby('precipitation_groups')['id'].count()
pre_gr_pas.plot(kind='bar')
plt.xlabel('Precipitation Group')
plt.ylabel('Number of Trips')
plt.title('Number of Trips by Precipitation Groups (10 levels)')
plt.show()

temp_inf = pd.read_csv('taxi_data/temp_inf.csv')  # corr temp / count
temp_inf.plot(kind='bar', x='temp_group', y='avg_rides_per_day')
plt.xlabel('Temperature Group')
plt.ylabel('Average Rides per Day')
plt.title('Average Rides per Day by Temperature Groups')
plt.show()

temp_inf = pd.read_csv('taxi_data/pre_inf.csv')  # corr precipit / count
temp_inf.plot(kind='bar', x='pre_group', y='avg_rides_per_day')
plt.xlabel('Precipitation Group')
plt.ylabel('Average Rides per Day')
plt.title('Average Rides per Day by Precipitation Groups')
plt.show()

#######################################################################################

plt.hist(merge_df['trip_duration'], bins=20, log=True)  # What is the most popular trip length?
plt.title('Trip Duration Histogram')
plt.xlabel('Trip Duration (seconds)')
plt.ylabel('Frequency')
plt.show()

########################################################################################

passenger_info = merge_df.groupby('passenger_count').agg(  # research on the number of passages per trip
    count=('passenger_count', 'count'),
    percentage=('passenger_count', lambda x: len(x) / len(merge_df) * 100))
plt.hist(merge_df['passenger_count'])
plt.show()

##############################################################################################

new_list = []  # most popular time of day
for i in range(24):
    new_list.append(i)

merge_df['hour'] = merge_df['pickup_datetime'].dt.hour
plt.hist(merge_df['hour'], bins=24)
plt.xticks(new_list)
plt.show()

merge_df['pickup_datetime'] = pd.to_datetime(merge_df['pickup_datetime'])  # most popular days
merge_df['Formatted_Date'] = merge_df['pickup_datetime'].dt.strftime('%B %d')
date_counts = merge_df['Formatted_Date'].value_counts().sort_index()
ax = date_counts.plot(kind='line')
ax.set_xticks(range(0, len(date_counts), 10))
ax.set_xticklabels(date_counts.index[::10], rotation=45, ha='right')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.title('Frequency of Pickups by Date')
plt.show()

###################################################################################################


counts = merge_df['vendor_id'].value_counts()  # percentage of suppliers
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

######################################################################################################

counts = merge_df['store_and_fwd_flag'].value_counts()  # data persistence
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

# ############################################################################################################

plt.hist(merge_df['distance_km'], range=(0, 20), bins=20)  # diagonal distance
plt.show()

counts = sample_df.groupby('BoroName_d')['BoroName_d'].count()  # most common landing site
counts.plot(kind='bar')
plt.show()

counts = sample_df.groupby('NATName_d')['NATName_d'].count()  # most common landing site
most_pop = counts.sort_values(ascending=False).head(10)
most_pop.plot(kind='bar')
plt.xticks(rotation=45, ha='right')
plt.show()

########################################################################################################

merge_df.plot.scatter(x='trip_duration', y='distance_km')  # trip duration and diagonal length
plt.show()

counts = merge_df.groupby('passenger_count')['trip_duration'].mean()  # number of passengers and trip duration
counts.plot(kind='bar')
plt.show()

data = pd.read_csv('taxi_data/sql_nat_time.csv')  # popular areas by season
data['season'] = data['season'].str.lower()
top_10_districts = data.groupby('NATName_p')['gen_cnt'].max().nlargest(10).index
filtered_data = data[data['NATName_p'].isin(top_10_districts)]
pivot_data = filtered_data.pivot_table(index='NATName_p', columns='season', values='cnt', fill_value=0)
plt.figure(figsize=(14, 8))
pivot_data[['summer', 'winter', 'spring']].plot(kind='bar', stacked=False)
plt.title('Top 10 Districts by Season Counts')
plt.xlabel('District')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Season')
plt.tight_layout()
plt.show()

#################################################################################################################

date_duration = pd.read_csv('taxi_data/date_duration.csv')  # duration of trip from day
date_duration.plot(kind='line', x='date', y='duration')
plt.show()

date_duration = pd.read_csv('taxi_data/date_ven.csv')  # supplier from day
date_duration.plot(kind='line', x='date', y=['ven_1', 'ven_2'])
plt.show()


pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)
weather = pd.read_csv('taxi_data/data/weather.csv')
weather['date'] = pd.to_datetime(weather['date'], infer_datetime_format=True, dayfirst=True)

df = weather
df['precipitation_n'] = df['precipitation'].replace('T', 0.05).astype(float)
df['snow fall_n'] = df['snow fall'].replace('T', 0.05).astype(float)
df['snow depth_n'] = df['snow depth'].replace('T', 0.05).astype(float)
# df.to_csv('test2_df.csv', index=False)

weather.plot(kind  = 'line', x = 'date', y =['average temperature', 'maximum temperature','minimum temperature'])

df.plot(kind  = 'line', x = 'date', y ='precipitation_n')
winter_df = df
condition = winter_df['date'].dt.month.isin([1, 2])
winter_df.loc[condition, 'date'] = winter_df.loc[condition, 'date'] + pd.DateOffset(years=1)
winter_df = winter_df.query(
    '(date >= "2016-12-01" and date <= "2017-02-28")'
)
winter_df.plot(kind  = 'line', x = 'date', y =['snow fall_n','snow depth_n', 'precipitation_n'])

seasons = pd.read_csv('taxi_data/temp_per.csv')
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='mean', hue='month', data=seasons, palette='magma', edgecolor='black')

