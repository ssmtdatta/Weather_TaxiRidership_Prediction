"""
This code scrapes historical hourly weather data
from Weather Underground.

The URL for the page is:
"https://www.wunderground.com/history/"

The user specifies a date range.
The hourly weather information for that date range is srcaped and 
stored in a pickle file.
"""



# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import bs4

import requests

import os

import time

import pandas as pd

from datetime import datetime as dt

import pickle

import scrape_module as smod



# URL of the website 
base_url = "https://www.wunderground.com/history/"

# start chrome driver
chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

#request page
driver.get(base_url)

# enter location - zipcode 60611
location_form = driver.find_element_by_name("code")
location_form.send_keys('60611')
location_form.send_keys(Keys.RETURN)



# the location for saving the scraped data
data_path = '~/ScrapedData/'


def getWeatherData(pickle_filename, date_range):
	
	month_df = pd.DataFrame()

	for d in date_range:

		print(d)

		enter_year, enter_month, enter_day = smod.dateString(d)
		date_string = enter_year+'/'+enter_month+'/'+enter_day
		smod.historyDate(driver, enter_year, enter_month, enter_day)
		page_url = driver.current_url
		# start scraping
		soup=BeautifulSoup(requests.get(page_url).text, 'html.parser')
		time.sleep(1)

		day_dictionary = smod.scrapeSoup(soup, date_string)
		day_df = pd.DataFrame(day_dictionary)
		month_df = pd.concat([month_df, day_df], axis=0)
	
	with open(data_path+pickle_filename, 'wb') as picklefile:
		pickle.dump(month_df, picklefile)



# scrape weather data for a date range
# data will be stored in a pickle file
pickle_filename = 'w_2016_january.p'
date_range = pd.date_range(start="01/01/2013", end = "01/31/2013", freq="1D")

getWeatherData(pickle_filename, date_range)








	
	






