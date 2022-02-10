import requests

import sys

sys.path.append(r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils")
import secret

# cities = ["Lisbon", "Warsaw", "Rome"]
# cities = ["Caen"]
cities = ["Lyon"]

# years_list = ["2015", "2016", "2017"]
# # cities = ["Caen", "Lyon", "Marseille"]
# key = secret.key6

# years_list = ["2018", "2019", "2020"]
# cities = ["Paris", "Lyon", "Marseille"]
# key = secret.key5

# years_list = ["2015","2016"]
# cities = ["Krakow", "Berlin"]
# key = secret.key4

# years_list = ["2017", "2018", "2019"]
# # cities = ["Krakow", "Berlin"]
# key = secret.key3

# years_list = ["2015"]
# cities = ["Krakow", "Berlin"]
# key = secret.key2

years_list = ["2014"]
# cities = ["Krakow", "Berlin"]
key = secret.key1



base_path = r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\data\weather"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

querystring = {
    "unitGroup": "metric",
    "elements": "datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,tempmax,tempmin,temp,humidity,precip,precipprob,precipcover,preciptype,snow,snowdepth,windgust,windspeed,winddir,pressure,cloudcover,visibility,solarradiation,solarenergy,uvindex,conditions,description",
    "include": "days",
    "key": key,
    "contentType": "json",
}

for year in years_list:
    from_date = year + "-01-01"
    to_date = year + "-12-31"

    for city in cities:
        output = f"{base_path}/{city}.{from_date}.{to_date}.json"
        print(output)

        try:
            f = open(output, "xb")
        except FileExistsError:
            print(f"Already retrieved : {output}")
            continue

        url = f"{base_url}/{city}/{from_date}/{to_date}"
        response = requests.request("GET", url, params=querystring)
        f.write(response.content)
        f.close()
