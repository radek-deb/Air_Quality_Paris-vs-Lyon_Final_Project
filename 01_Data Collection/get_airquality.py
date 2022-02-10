import requests

# https://aqicn.org/data-platform/covid19/

base_path = r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\data\airquality"

url_tuples = [
    ("waqi-covid-2020.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2020"),
    ("waqi-covid-2021Q1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2021Q1"),
    ("waqi-covid-2021Q2.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2021Q2"),
    ("waqi-covid-2021Q3.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2021Q3"),
    ("waqi-covid-2021Q4.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2021Q4"),
    ("waqi-covid-2020Q1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2020Q1"),
    ("waqi-covid-2020Q2.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2020Q2"),
    ("waqi-covid-2020Q3.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2020Q3"),
    ("waqi-covid-2020Q4.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2020Q4"),
    ("waqi-covid-2019Q1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2019Q1"),
    ("waqi-covid-2019Q2.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2019Q2"),
    ("waqi-covid-2019Q3.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2019Q3"),
    ("waqi-covid-2019Q4.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2019Q4"),
    ("waqi-covid-2018H1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2018H1"),
    ("waqi-covid-2017H1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2017H1"),
    ("waqi-covid-2016H1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2016H1"),
    ("waqi-covid-2015H1.csv", "https://aqicn.org/data-platform/covid19/report/34644-0654e09a/2015H1"),
]

for (name, url) in url_tuples:
    output = f"{base_path}/{name}"
    print(f"Downloading {url} to {output}")
    f = open(output, "wb")
    response = requests.request("GET", url)
    f.write(response.content)
    f.close()
