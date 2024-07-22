# Group 3 - Exploratory Data Analysis (EDA) Project 1

## Team Members
* Jim Gile
* Anna Fine
* Carl Peterson
* Tim Willard

## Roles
* Git master: Jim
* Presentation Design: Anna 
* Data Sourcing: Jim, Anna, Carl, Tim
* Coding & Analysis: Jim, Anna - with input from Tim, Carl
* Presentation: Team Slice & Dice


## Project Overview
As a group we wanted to find a topic that was relevant to our interests, timely in the world, and with enough data to provide valid research for the project.  With that in mind, we set out to review Olympic medal count results over time to determine how strong the correlation was with  each country's happiness index, the country's overall GDP, and the availability of an adequate diet of the population. 

Our hypothesises was that there would be a strong correlation among all three and that the happier countries, those with greater GDP's, and those with higher adequate diet would have larger overall medal counts. In order to determine if this was accurate; we needed to analyze and compare Olympic data from Kaggle, GDP & diet information from World Bank, and the World Happiness index for each country.  We then had to clean up the data to be able to compare across each data set and come up with any correlations that existed.  

During the process we found some team learnings in utilizing classes and functions to streamline processing, pivoting research analysis to match available data, the ability to change midstream when data was inaccessible or expensive to obtain, and the importance of good repository management.

Questions to answer:
  * What are the most awarded counties by medal, year and select events?
  * What, if any, is the relationship between happiness and the Olympics?
  * What, if any, is the relationship between the GDP and the Olympics?
  * What, if any, is the relationship between nutrition and the Olympics?
  * How strong are these correlations?

## Sourced Data
Kaggle - Olympic Data 

- [Olympic Summer & Winter Games, 1896-2022](https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018)
- [olympic-data](https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data)
- [olympic-games-medals-19862018](https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018)
- [Olympics Legacy: 1896-2020](https://www.kaggle.com/datasets/krishd123/olympics-legacy-1896-2020)
- [Olympics Althlete Events Analysis](https://www.kaggle.com/datasets/samruddhim/olympics-althlete-events-analysis)
- [Summer Olympics Medals (1976-2008)](https://www.kaggle.com/datasets/divyansh22/summer-olympics-medals)

World Happiness
- [World-Happiness-Report](https://worldhappiness.report/data/)

World Bank - GDP & Nutrition
- [GDP](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)
- [Nutrition](https://databank.worldbank.org/source/food-prices-for-nutrition/Type/TABLE/preview/on)

## Installation
1. Clone the Repository  - git clone git@github.com:JimGile/group3-project1.git
2. Create a virtual environment - python -m venv venv
3. Activate the virtual environment - venv\Scripts\activate
4. pip install pandas, numpy, plotly, matplotlib, seaborn, jupyter

The following files will be found in the repository and can be loaded using similar installation instructions:

## Kaggle Olympic Games Medals Analysis Class
The olympic data was extensive and had various files to find the information required.  Do to the need for simplifying, Jim created a class that could be used throughout the project. The `KaggleOlympicGamesMedals` class helps to process and visualize this data.

Usage
Class: KaggleOlympicGamesMedals
This class provides methods to process and visualize Olympic Games medals data.

Methods
1.  `__init__(self, medals_file: str, hosts_file: str)`
  * Initializes the class with medals and hosts data files.
  * Parameters:
    * medals_file (str): Path to the CSV file containing medals data.
    * hosts_file (str): Path to the CSV file containing hosts data.
2. `load_data(self)`
  * Loads the medals and hosts data into DataFrames.
3. `_merge_hosts(self, df: pd.DataFrame) -> pd.DataFrame`
  * Merges the hosts data with the medals data.
  * Parameters:
    * df (pd.DataFrame): DataFrame containing medals data.
  * Returns: Merged DataFrame.
4. `_clean_data(self, df: pd.DataFrame) -> pd.DataFrame`
  * Cleans the merged DataFrame by setting game locations.
  * Parameters:
    * df (pd.DataFrame): Merged DataFrame.
  * Returns: Cleaned DataFrame.
5. `get_medals(self) -> pd.DataFrame`
  * Returns a copy of the medals DataFrame.
6. `get_medals_by_country(self) -> pd.DataFrame`
  * Returns medals data grouped by country.
7. `get_country_name_codes(self) -> pd.DataFrame`
  * Returns a DataFrame containing country names and codes.
8. `plot_country_medals(self, df: pd.DataFrame, country: str, season: str, figsize=(16, 16), save=False)`
  * Plots a heatmap of medals for a specific country and season.
  * Parameters:
    * df (pd.DataFrame): DataFrame containing medals data.
    * country (str): Country name.
    * season (str): Season ('Summer' or 'Winter').
    * figsize (tuple, optional): Size of the figure.
    * save (bool, optional): Save the plot as an image.
9. `plot_country_discipline_gender_medal_heatmap(self, df: pd.DataFrame, season: str, country: str, discipline: str, gender: str, figsize=(16, 16), save=False)`
  * Plots a heatmap of medals for a specific country, discipline, and gender.
  * Parameters:
    * df (pd.DataFrame): DataFrame containing medals data.
    * season (str): Season ('Summer' or 'Winter').
    * country (str): Country name.
    * discipline (str): Discipline name.
    * gender (str): Gender ('Men' or 'Women').
    * figsize (tuple, optional): Size of the figure.
    * save (bool, optional): Save the plot as an image.

 ##  Olympic Games Data Visualization     
Overview:
This Jupyter Notebook, `olympic_games_data_vis.ipynb`, provides a comprehensive analysis and visualization of Olympic Games data. It integrates various datasets to deliver insights into medal distributions, country performances, and historical trends in the Olympics.

Requirements:
  * pandas
  * numpy
  * matplotlib
  * seaborn
  * plotly

Data Sources:
  * Olympic medals data
  * World happiness data
  * Nutrition data
  * GDP data
(All data acquired from additional notebook files below)

Features:
  * Data cleaning and preprocessing
  * Merging multiple datasets
  * Analysis of Olympic medal distributions by country, year, and event
  *Visualization of trends and patterns using various plotting libraries

Results:
The notebook will produce a series of plots and charts that illustrate key insights from the Olympic Games data, including:
  * Medal counts by country and year
  * Trends in country performance over time
  * Correlations between world happiness, nutrition, GDP, and Olympic success

## Olympic Games Medal Type Analysis with Games
Overview:
This Jupyter Notebook, `jg_medal_type_analysis_with_games.ipynb`, provides an analysis of Olympic medals by type (gold, silver, bronze) across different games. The notebook explores trends and patterns in medal distributions over various Olympic events.

Requirements:
  * pandas
  * seaborn
  * matplotlib - pyplot

Data Files:
  * olympic_medals.csv
  * games_data.csv

Features:
  * Load the datasets into pandas DataFrames.
  * Handle missing values, duplicates, and inconsistent data.
  * Explore medal distributions by type and game.
  * Generate plots and charts to visualize the findings.

Results:
  * Cleaned and analyzed datasets.
  * Insightful visualizations showing trends in medal distributions by type and game.
  * A deeper understanding of how different games contribute to medal counts.

## Simplified Analysis of Olympic Medal Details
Overview:
This Jupyter Notebook, `jg_medal_detail_corr_simplified.ipynb`, provides a simplified analysis of the correlations between various factors and Olympic medal counts. It focuses on examining the relationships between medal counts and factors like GDP, nutrition, and world happiness.

Requirements:
  * pandas
  * numpy
  * seaborn
  * matplotlib

Data Files:
  * olympic_medals.csv
  * world_happiness.csv
  * nutrition_data.csv
  * gdp_data.csv

Features:
  * Load the datasets into pandas DataFrames.
  * Handle missing values, duplicates, and inconsistent data.
  * Analyze the correlations between medal counts and various factors.
  * Generate plots and charts to visualize the findings.

Results:
  * Cleaned and analyzed datasets.
  * Insightful visualizations showing correlations between medal counts and factors like GDP, nutrition, and happiness.
  * A simplified understanding of how these factors relate to Olympic success.
  
## Olympic Medal Type Correlation with Games
Overview:
This Jupyter Notebook, `jg_medal_type_correlation_with_games.ipynb`, provides an analysis of the correlation between different types of Olympic medals (gold, silver, bronze) and various Olympic Games. The notebook aims to uncover trends and patterns in medal distributions across different events and games.

Requirements:
  * pandas
  * seaborn
  * matplotlib - pyplot

Data Files:
  * olympic_medals.csv
  * games_data.csv

Features:
  * Load the datasets into pandas DataFrames.
  * Handle missing values, duplicates, and inconsistent data.
  * Analyze the correlations between different medal types and Olympic Games.
  * Generate plots and charts to visualize the findings.

Results:
  * Cleaned and analyzed datasets.
  * Insightful visualizations showing trends in medal types across different Olympic Games.
  * A deeper understanding of how different games and events correlate with medal distributions.

## Olympic Medal Detail Correlations
Overview
This Jupyter Notebook, `jg_medal_detail_correlations.ipynb`, analyzes correlations between various factors (like GDP, nutrition, and world happiness) and Olympic medal counts. The goal is to uncover patterns and insights that can explain country performances in the Olympic Games.

Requirements:
  * pandas
  * seaborn
  * numpy
  * matplotlib

Data Files:
  * olympic_medals.csv
  * world_happiness.csv
  * nutrition_data.csv
  * gdp_data.csv

Features:
  * Load the datasets into pandas DataFrames.
  * Handle missing values, duplicates, and inconsistent data.
  * Analyze the correlations between medal counts and various factors.
  * Generate plots and charts to visualize the findings. 

Results:
  * Cleaned and analyzed datasets.
  * Insightful visualizations showing correlations between medal counts and factors like GDP, nutrition, and happiness.
  *  A deeper understanding of how these factors relate to Olympic success.

## Merging Olympic Datasets
Overview:
This Jupyter Notebook, `jg_merge_datasets.ipynb`, demonstrates how to merge multiple Olympic-related datasets to create a comprehensive dataset for further analysis. The notebook combines data on Olympic medals, world happiness, nutrition, and GDP.

Requirements: 
  * pandas
  * numpy
  * seaborn
  * matplotlib

Data Files:
  * olympic_medals.csv
  * world_happiness.csv
  * nutrition_data.csv
  * gdp_data.csv

Features:
  * Load the datasets into pandas DataFrames.
  * Handle missing values, duplicates, and inconsistent data.
  * Merge datasets to create a comprehensive DataFrame for analysis.
  * Initial data exploration using descriptive statistics and visualizations.

Results:
  * Cleaned and merged datasets.
  * A comprehensive DataFrame that integrates Olympic medals, world happiness, nutrition, and GDP data.

## World Happiness Analysis
Overview:
This Jupyter Notebook, `world_happiness.ipynb`, provides an analysis of the World Happiness Report data. The notebook explores trends and patterns in happiness scores across different countries and examines factors that contribute to overall happiness.

Requirements:
  * pandas
  * numpy
  * seaborn
  * matplotlib

Data Files:
  * world_happiness_data.csv

Features:
  * Load the World Happiness Report data into a pandas DataFrame.
  * Handle missing values, duplicates, and inconsistent data.
  * Initial data exploration using descriptive statistics and visualizations.
  * Analyze the factors contributing to happiness scores.
  * Generate plots and charts to visualize the findings.

Results:
  * Cleaned and analyzed World Happiness Report data.
  * Insightful visualizations showing trends and patterns in happiness scores.
  * A deeper understanding of the factors that contribute to happiness across different countries. 

##  Nutrition Data Cleaning
Overview:
This Jupyter Notebook, `jg_clean_nutrition.ipynb`, focuses on cleaning and preprocessing nutrition data. The notebook handles missing values, duplicates, and inconsistent data to prepare the dataset for further analysis.

Requirements:
  * pandas
  * numpy

Data Files:
  * nutrition_data.csv

Features:
  * Load the nutrition data into a pandas DataFrame.
  * Handle missing values, duplicates, and inconsistent data.
  * Perform necessary transformations to standardize the dataset.
  * Initial data exploration using descriptive statistics and visualizations to verify the cleaning process.

Results:
  * A cleaned and standardized nutrition dataset ready for further analysis.

##  World Bank GDP Analysis (1960-2023)
Overview:
This Jupyter Notebook, `World_Bank_GDP_1960_2023.ipynb`, provides an analysis of the World Bank GDP data from 1960 to 2023. The notebook explores trends and patterns in GDP across different countries and examines economic growth over time.

Requirements:
  * pandas
  * numpy
  * seaborn
  * matplotlib

Features:
  * Load the World Bank GDP data into a pandas DataFrame.
  * Handle missing values, duplicates, and inconsistent data.
  * Initial data exploration using descriptive statistics and visualizations.
  * Analyze GDP trends and growth patterns over time.
  * Generate plots and charts to visualize the findings.

Results:
  * Cleaned and analyzed World Bank GDP data from 1960 to 2023.
  * Insightful visualizations showing GDP trends and economic growth patterns.
  * A deeper understanding of the economic performance of different countries over time.

## Summary of Analysis
We went into this project with the expectation that happiness levels, adequate diet, and overall country GDP would have all been highly correlated with the country winning gold medals.  What we found was a very strong correlation between GDP and winning a medal in the olypics, however there was not nearly as storng a correlation with adequate diet and happiness as we expected. 

## Project Learnings
During this project we discovered a few learning, both good and bad, that will help for any future endeavors we take on:
  * Creating classes and functions will help stremaline processes and prevent repeating the same work over an over
  * Some findings cannot be discovered until the data is reviewed thouroughly, and once discovered could change the course of the work
  * Not all data is created equal and sometimes cannot be used even when seemingly perfect for the task
  * Utilizing branching in a repository has major benefits, but is also difficult for early programmers
  * It's ok to pivot and change after seeing the data available to work with.

## If we were to continuee...
If there was more time to continue on this effort we would have taken the time to breakdown the data further and test our hypothesises at a more macro level on specific events and potentially individula athletes to see if there would have been any difference in the correlations with GDP, Diet, and happiness.


