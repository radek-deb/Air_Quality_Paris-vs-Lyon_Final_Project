import sys
sys.path.append(r'C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils')

import db_utils as db

airquality_tmp_drop = """
DROP TABLE `airquality_tmp`;
"""

airquality_drop = """
DROP TABLE `airquality`;
"""

airquality_tmp_create = """
CREATE TABLE `airquality_tmp` (
	`Date` Datetime,
	`Country` varchar(50),
	`City` varchar(50),
	`co_min` double DEFAULT NULL,
	`no2_min` double DEFAULT NULL,
	`o3_min` double DEFAULT NULL,
	`pm10_min` double DEFAULT NULL,
	`pm25_min` double DEFAULT NULL,
	`so2_min` double DEFAULT NULL,
	`co_max` double DEFAULT NULL,
	`no2_max` double DEFAULT NULL,
	`o3_max` double DEFAULT NULL,
	`pm10_max` double DEFAULT NULL,
	`pm25_max` double DEFAULT NULL,
	`so2_max` double DEFAULT NULL,
	`co_median` double DEFAULT NULL,
	`no2_median` double DEFAULT NULL,
	`o3_median` double DEFAULT NULL,
	`pm10_median` double DEFAULT NULL,
	`pm25_median` double DEFAULT NULL,
	`so2_median` double DEFAULT NULL,
	`co_variance` double DEFAULT NULL,
	`no2_variance` double DEFAULT NULL,
	`o3_variance` double DEFAULT NULL,
	`pm10_variance` double DEFAULT NULL,
	`pm25_variance` double DEFAULT NULL,
	`so2_variance` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

airquality_create = """
CREATE TABLE `airquality` (
	`Date` Datetime,
	`Country` varchar(50),
	`City` varchar(50),
	`co_min` double DEFAULT NULL,
	`no2_min` double DEFAULT NULL,
	`o3_min` double DEFAULT NULL,
	`pm10_min` double DEFAULT NULL,
	`pm25_min` double DEFAULT NULL,
	`so2_min` double DEFAULT NULL,
	`co_max` double DEFAULT NULL,
	`no2_max` double DEFAULT NULL,
	`o3_max` double DEFAULT NULL,
	`pm10_max` double DEFAULT NULL,
	`pm25_max` double DEFAULT NULL,
	`so2_max` double DEFAULT NULL,
	`co_median` double DEFAULT NULL,
	`no2_median` double DEFAULT NULL,
	`o3_median` double DEFAULT NULL,
	`pm10_median` double DEFAULT NULL,
	`pm25_median` double DEFAULT NULL,
	`so2_median` double DEFAULT NULL,
	`co_variance` double DEFAULT NULL,
	`no2_variance` double DEFAULT NULL,
	`o3_variance` double DEFAULT NULL,
	`pm10_variance` double DEFAULT NULL,
	`pm25_variance` double DEFAULT NULL,
	`so2_variance` double DEFAULT NULL,
	PRIMARY KEY(`Date`, `Country`, `City`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

db.exec(airquality_tmp_drop)
db.exec(airquality_drop)
db.exec(airquality_tmp_create)
db.exec(airquality_create)
