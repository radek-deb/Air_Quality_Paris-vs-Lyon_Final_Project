import sys

sys.path.append(r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils")

import db_utils as db

weather_tmp_drop = """
DROP TABLE `weather_tmp`;
"""
weather_drop = """
DROP TABLE `weather`;
"""

weather_tmp_create = """
CREATE TABLE `weather_tmp` (
	`latitude` double DEFAULT NULL,
	`longitude` double DEFAULT NULL,
	`address` varchar(50),
	`datetime` Datetime,
	`datetimeEpoch` bigint(20) DEFAULT NULL,
	`tempmax` double DEFAULT NULL,
	`tempmin` double DEFAULT NULL,
	`temp` double DEFAULT NULL,
	`humidity` double DEFAULT NULL,
	`precip` double DEFAULT NULL,
	`precipcover` double DEFAULT NULL,
	`snow` varchar(50) DEFAULT NULL,
	`snowdepth` double DEFAULT NULL,
	`windgust` double DEFAULT NULL,
	`windspeed` double DEFAULT NULL,
	`pressure` double DEFAULT NULL,
	`cloudcover` double DEFAULT NULL,
	`visibility` double DEFAULT NULL,
	`solarradiation` double DEFAULT NULL,
	`solarenergy` double DEFAULT NULL,
	`uvindex` double DEFAULT NULL,
	`conditions` varchar(100) DEFAULT NULL,
	`description` varchar(100) DEFAULT NULL
) engine=InnoDB DEFAULT CHARSET=utf8mb4;
"""

weather_create = """
CREATE TABLE `weather` (
	`latitude` double DEFAULT NULL,
	`longitude` double DEFAULT NULL,
	`address` varchar(50),
	`datetime` Datetime,
	`datetimeEpoch` bigint(20) DEFAULT NULL,
	`tempmax` double DEFAULT NULL,
	`tempmin` double DEFAULT NULL,
	`temp` double DEFAULT NULL,
	`humidity` double DEFAULT NULL,
	`precip` double DEFAULT NULL,
	`precipcover` double DEFAULT NULL,
	`snow` varchar(50) DEFAULT NULL,
	`snowdepth` double DEFAULT NULL,
	`windgust` double DEFAULT NULL,
	`windspeed` double DEFAULT NULL,
	`pressure` double DEFAULT NULL,
	`cloudcover` double DEFAULT NULL,
	`visibility` double DEFAULT NULL,
	`solarradiation` double DEFAULT NULL,
	`solarenergy` double DEFAULT NULL,
	`uvindex` double DEFAULT NULL,
	`conditions` varchar(100) DEFAULT NULL,
	`description` varchar(100) DEFAULT NULL,
	PRIMARY KEY(`datetime`, `address`)
) engine=InnoDB DEFAULT CHARSET=utf8mb4;
"""

db.exec(weather_tmp_drop)
db.exec(weather_drop)
db.exec(weather_tmp_create)
db.exec(weather_create)
