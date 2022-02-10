import sys
sys.path.append(r'C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils')

import db_utils as db

airquality_tmp_drop = """
DROP TABLE `airquality_tmp_v2`;
"""

airquality_drop = """
DROP TABLE `airquality_v2`;
"""

airquality_tmp_create = """
CREATE TABLE `airquality_tmp_v2` (
  `date` Datetime,
  `pm25` double DEFAULT NULL,
  `pm10` double DEFAULT NULL,
  `o3` double DEFAULT NULL,
  `no2` double DEFAULT NULL,
  `so2` double DEFAULT NULL,
  `co` double DEFAULT NULL,
  `City` varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

airquality_create = """
CREATE TABLE `airquality_v2` (
  `date` Datetime,
  `pm25` double DEFAULT NULL,
  `pm10` double DEFAULT NULL,
  `o3` double DEFAULT NULL,
  `no2` double DEFAULT NULL,
  `so2` double DEFAULT NULL,
  `co` double DEFAULT NULL,
  `City` varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

db.exec(airquality_tmp_drop)
db.exec(airquality_drop)
db.exec(airquality_tmp_create)
db.exec(airquality_create)
