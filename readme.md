<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Final Project | Air Quality
*[Radoslaw Debek]*

*[Data Analytics, Paris, 11.02.2022]*

## Content
- [Final Project | Air Quality](#final-project--air-quality)
	- [Content](#content)
	- [Project Description](#project-description)
	- [Workflow](#workflow)
	- [Deploying to Heroku](#deploying-to-heroku)
	- [Links](#links)

## Project Description
Air quality forecast in Paris

Business problem: Forecast of air quality in Paris in coming months basing on the historical data (priod from 2014 till the end of 2021).

The two approaches will be used in the project. Time series analysis of 4 pollutants pm2.5, pm10, NO2 and O3.
Machine learning in order to predict the airquality on a specific day given the weather conditions and month.

## Workflow

1. Building a databese with the historical data on air quality and weather conditions for the selected cities in Europe.
    1.1. Data Collection:
    - air pollution data: <https://aqicn.org/>
    - weather data: <https://weather.visualcrossing.com/>
    1.2. Loading data into the database:
    - formating of the files
    - adding data into SQL database
2. Data Selection:
   - selection of the data for a specific city (i.e. Paris)
   - wriitng a SQL query and importing the data into Pythob
3. Data Cleaning and Processig
   - claening and processing of data for Time Series Analysis
   - cleaning and processing of data for Machine Learning
4. Time Series Analysis
5. Machine Learning
6. Models testing.
7. Comparison of air pollution in Paris with diffrent cities in Europe.
8. Creating Dashboard.
9. Preparing deliverables (readme file, Git-Hub repository, presenation).

## Deploying to Heroku

```bash
heroku git:remote -a air-quality-final-project
git subtree push --prefix "08 - Streamlit" heroku main
```

## Links

[Dashboard])
[Repository]()
[Slides]()
[Trello](https://trello.com/b/vJ5wxT1K/finalprojectradek)
