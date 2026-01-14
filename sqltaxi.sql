WITH period AS (
	SELECT id, pickup_datetime, STRFTIME('%y', pickup_datetime) AS year, STRFTIME('%m', pickup_datetime) AS month, 
		STRFTIME('%d', pickup_datetime) AS day, STRFTIME('%H', pickup_datetime) as hours, STRFTIME('%H:%M:%S', pickup_datetime) as time,  
		STRFTIME('%m-%d', pickup_datetime) AS date,
		CASE 
			WHEN STRFTIME('%m', pickup_datetime) IN ('12', '01', '02')
			THEN 'winter'
			WHEN STRFTIME('%m', pickup_datetime) BETWEEN '03' AND '05'
			THEN 'spring'
			WHEN STRFTIME('%m', pickup_datetime) BETWEEN '06' AND '09'
			THEN 'summer'
			ELSE 'autumn'
			END season,
		CASE 
           WHEN STRFTIME('%w', pickup_datetime) IN ('0', '6') THEN 'yes'
           ELSE 'no'
       END AS is_holiday
	FROM 'data/train.csv')

	
SELECT month, COUNT(month) AS cnt, ROUND(COUNT(month) / (SELECT COUNT(*) FROM period) * 100,2) -- the busiest months
FROM period
GROUP BY month;

-- SELECT day, COUNT(day) AS cnt, ROUND(COUNT(day) / (SELECT COUNT(*) FROM period) * 100,2) AS prc  -- the busiest dates
-- FROM period
-- GROUP BY day
-- ORDER BY prc DESC;

-- SELECT *,             --   difference between seasons
-- 	CASE
-- 		WHEN season = 'spring'
-- 		THEN prc / 3
-- 		WHEN season = 'winter'
-- 		THEN prc / 2
-- 		ELSE prc
-- 		END 
-- FROM(
-- 	SELECT season, COUNT(season) AS cnt, ROUND(COUNT(season) / (SELECT COUNT(*) FROM period) * 100,2) AS prc
-- 	FROM period
-- 	GROUP BY season
-- )Q

-- SELECT is_holiday,    --difference between weekends
--   CASE 
--   	WHEN is_holiday = 'yes'
-- 	THEN COUNT(*) / 2
-- 	ELSE COUNT(*) / 5
-- 	END prc
-- FROM (
-- 	SELECT pickup_datetime, is_holiday, COUNT(day) AS cnt
-- 	FROM period
-- 	GROUP BY pickup_datetime, is_holiday
-- )Q
-- GROUP BY is_holiday;

-- SELECT STRFTIME('%m-%d', pickup_datetime) AS year_month, COUNT(*) --most popular months-days
-- FROM 'data/train.csv'
-- GROUP BY year_month;

-- SELECT STRFTIME('%H', pickup_datetime) AS hhh, COUNT(*)  --most popular hours
-- FROM 'data/train.csv'
-- GROUP BY hhh;

-- --------------------------------------------------------------------------------------

-- SELECT passenger_count, COUNT(passenger_count) -- passenger number survey
-- FROM 'data/train.csv'
-- GROUP BY passenger_count
-- ORDER BY passenger_count;

-- ----------------------------------------------------------------------------------------

-- SELECT time, COUNT(time) AS q  --travel duration research
-- FROM (
-- 	SELECT trip_duration, ROUND(trip_duration, -2) AS time
-- 	FROM 'data/train.csv'
-- )
-- GROUP BY time
-- ORDER BY q DESC;

-- ------------------------------------------------------------------------------------------

-- SELECT vendor_id, COUNT(*), ROUND(COUNT(*)/(SELECT COUNT(*) FROM 'data/train.csv')*100,2) -- percentage of suppliers
-- FROM 'data/train.csv'
-- GROUP BY vendor_id;

-- ------------------------------------------------------------------------------------------

-- SELECT store_and_fwd_flag, COUNT(*), ROUND(COUNT(*)/(SELECT COUNT(*) FROM 'data/train.csv')*100,2)    --data persistence
-- FROM 'data/train.csv'
-- GROUP BY store_and_fwd_flag;

-- ----------------------------------------------------------------------------------------

-- SELECT distance, COUNT(distance) AS cnt    --most popular distances 
-- FROM (
-- 	SELECT ROUND(distance_km * 2) / 2 AS distance
-- 	FROM test_df.csv
-- )Q
-- GROUP BY distance
-- ORDER BY cnt DESC;

-- WITH rout AS (                                                                
-- 	SELECT NATName_p, NATName_d, COUNT(*) AS cnt
-- 	FROM 'test_df.csv'
-- 	GROUP BY NATName_p, NATName_d
-- )

-- SELECT *            -- the most popular one-way routes
-- FROM rout;

-- SELECT *, A.cnt+B.cnt AS summ   -- the most popular routes in both directions
-- FROM rout A FULL JOIN rout B
-- ON A.NATName_p = B.NATName_d AND B.NATName_p = A.NATName_d
-- ORDER BY summ DESC;

-- ----------------------------------------------------------------------------------------

-- SELECT A.NATName_p, season, COUNT(*) AS cnt, ROUND(COUNT(*)/  -- quarters by season
-- 	(SELECT COUNT(*) FROM 'test_df.csv' C WHERE C.NATName_p = A.NATName_p) * 100,2) AS prc,
-- 	SUM(cnt) OVER (PARTITION BY A.NATName_p) AS gen_cnt
-- FROM 'test_df.csv' A INNER JOIN period B
-- ON A.id = B.id
-- GROUP BY A.NATName_p, season
-- ORDER BY A.NATName_p, season;


-- SELECT NATName_p, AVG(passenger_count) AS mean  -- quarters by number of passengers
-- FROM 'test_df.csv'
-- GROUP BY NATName_p
-- ORDER BY mean DESC;

-- SELECT NATName_p, AVG(trip_duration) AS mean   -- departure points with the longest time interval
-- FROM 'test_df.csv'
-- GROUP BY NATName_p
-- ORDER BY mean DESC;


-- SELECT NATName_d, AVG(passenger_count) AS mean   -- points of arrival with mothers over a long period of time
-- FROM 'test_df.csv'
-- GROUP BY NATName_d
-- ORDER BY mean DESC;

-- SELECT A.NATName_p, A.NATName_d,AVG(distance_km), AVG(trip_duration) -- distance
-- FROM rout A INNER JOIN 'test_df.csv' B
-- ON A.NATName_p = B.NATName_p AND A.NATName_d = B.NATName_d
-- GROUP BY A.NATName_p, A.NATName_d
-- ORDER BY AVG(distance_km) DESC;
-- ---------------------------------------------------------------------------------------

-- SELECT vendor_id, AVG(passenger_count)   -- which supplier carries how many passengers
-- FROM 'data/train.csv'
-- GROUP BY vendor_id;

-- SELECT passenger_count, AVG(trip_duration) AS mean   --duration of the trip depending on the number of passengers
-- FROM 'data/train.csv'
-- GROUP BY passenger_count
-- ORDER BY mean DESC;

-- ---------------------------------------------------------------------------------

-- SELECT season, month, AVG(trip_duration)      -- travel duration per month
-- FROM period A INNER JOIN 'data/train.csv' B
-- ON A.id = B.id
-- GROUP BY season, month
-- ORDER BY month;
 
-- SELECT is_holiday, AVG(trip_duration)  -- duration of trip on weekends
-- FROM period A INNER JOIN 'data/train.csv' B
-- ON A.id = B.id
-- GROUP BY is_holiday;

-- SELECT date, AVG(trip_duration) as duration    -- duration of the trip in calendar days
-- FROM period A INNER JOIN 'data/train.csv' B   -- for python export
-- ON A.id = B.id
-- GROUP BY date
-- ORDER BY date;

-- SELECT date, COUNT(B.id) AS ven_1, COUNT(C.id) AS ven_2
-- FROM period A LEFT JOIN 'data/train.csv' B               
-- ON A.id = B.id AND B.vendor_id = 1
-- LEFT JOIN 'data/train.csv' C
-- ON A.id = C.id AND C.vendor_id = 2
-- GROUP BY date
-- ORDER BY date;

-- SELECT date, COUNT(*)
-- FROM 'data/train.csv' A INNER JOIN period B
-- ON A.id = B.id
-- GROUP BY date

WITH period AS (
	SELECT date, STRFTIME('%m', date) AS month,
		CASE 
				WHEN STRFTIME('%m', date) IN ('12', '01', '02')
				THEN 'winter'
				WHEN STRFTIME('%m', date) BETWEEN '03' AND '05'
				THEN 'spring'
				WHEN STRFTIME('%m', date) BETWEEN '06' AND '09'
				THEN 'summer'
				ELSE 'autumn'
				END season
	FROM 'data/weather.csv'
)


SELECT season, month, ROUND(AVG("average temperature"),2) AS mean,          --temperature for each month/season 
	ROUND(AVG("minimum temperature"),2) AS minn, ROUND(AVG("maximum temperature"),2) AS maxx
FROM period A INNER JOIN 'data/weather.csv' B
ON A.date = B.date
GROUP BY ROLLUP (season, month)
ORDER BY month;

-- SELECT season, month, ROUND(AVG(precipitation_n),2) AS precipitation_nn,  -- precipitation for each month/season
-- 	ROUND(AVG("snow fall_n"),2) AS snow_fall_nn, ROUND(AVG("snow depth_n"),2) AS snow_depth_nn
-- FROM period A INNER JOIN 'test2_df.csv' B
-- ON A.date = B.date
-- GROUP BY ROLLUP (season, month)
-- ORDER BY month;

-- SELECT rounded_precipitation_n, COUNT(rounded_precipitation_n) AS cnt  -- precipitation amount divided into groups
-- FROM (
-- 	SELECT ROUND(precipitation_n * 4) / 4 AS rounded_precipitation_n
-- 	FROM 'test2_df.csv'
-- )Q
-- GROUP BY rounded_precipitation_n
-- HAVING rounded_precipitation_n <> 0
-- ORDER BY cnt DESC;
