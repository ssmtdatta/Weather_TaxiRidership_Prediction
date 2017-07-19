from collections import OrderedDict
import re
from datetime import datetime as dt


#global data_dict

dict_keys = ['date_time', 'temp', 'chill_heat',
              'dew', 'humidity' , 'pressure', 'visibility', 
              'wind_dir', 'wind_speed', 'gust', 'precipitation', 
              'event', 'condition']

def dateString(dt):
    _year, _month, _day = dt.year, dt.month, dt.day
   
    year_str = str(_year)
    month_str = str(_month)
    day_str = str(_day)
    
    if month_str[0] == '0':
        month_str = month_str[1]
    if day_str[0] == '0':
        day_str = day_str[1]
    
    return year_str, month_str, day_str

def historyDate(driver, enter_year, enter_month, enter_day):
	# select month
	driver.find_element_by_xpath(
    	"//select[@name='month']/option[@value=%s]" %(enter_month)).click()
	#select day
	driver.find_element_by_xpath(
    	"//select[@name='day']/option[text()=%s]" %(enter_day)).click()
	# select year
	driver.find_element_by_xpath(
    	"//select[@name='year']/option[text()=%s]" %(enter_year)).click()
	# click the view button (after selecting date) 
	driver.find_element_by_xpath(
    	"//input[@value='View' and @type='submit']").click()


def dateTimeConversion(d): 
    date_format = "%Y/%m/%d %I:%M %p" #'2016/1/1 12:53 AM'
    x = dt.strptime(d, date_format)
    return x

def createEmptyDictionary():
	data_dict = OrderedDict()
	dict_keys = ['date_time', 'temp', 'chill_heat',
              'dew', 'humidity' , 'pressure', 'visibility', 
              'wind_dir', 'wind_speed', 'gust', 'precipitation', 
              'event', 'condition']
	for key in dict_keys:
		data_dict[key] = []
	return data_dict

def writeDict(scraped_info, data_dict, date_string):
    for k in range(0, len(dict_keys)):
        if k == 0:
            info = date_string + ' ' + scraped_info[k]
            info = dateTimeConversion(info)
        else:
            info = scraped_info[k]
        data_dict[dict_keys[k]].append(info)
    return data_dict


def scrapeSoupItem(soup_item):
    scraped = []
    children = soup_item.findChildren('td')
    for ch in children:
        if not (ch.findChild(class_="wx-value")):
            scraped.append(ch.text)
        elif ch.findChild(class_="wx-value"):
            value = ch.findChild(class_="wx-value")
            scraped.append(value.text)   
        else:
            scraped.append("missing")
    return scraped

def cleanUp(scraped_info):
    scraped_info = list(map(lambda x: re.sub(r'[\t\r\n\f]', "", x), scraped_info))
    scraped_info = list(map(lambda x: x.replace('\xa0', '-'), scraped_info))
    scraped_info = list(map(lambda x: x.replace('%', ''), scraped_info))
    scraped_info = list(map(lambda x: x.replace('N/A', '0'), scraped_info))
    scraped_info = list(map(lambda x: x.replace('-', '0'), scraped_info)) 
    scraped_info[8] = re.sub(r'[a-zA-Z]', "0", scraped_info[8] )
    scraped_info = [float(scraped_info[i]) 
                    if i in [1, 2, 3, 4, 5, 6, 8, 9, 10] 
                    else scraped_info[i] 
                    for i in range(0, len(scraped_info)) ]
    return scraped_info
    
def scrapeSoup(soup, date_string):
    data_dict = createEmptyDictionary() # a new dictionary is created
    soup_find_all = soup.find_all('tr', class_='no-metars')
    for i in range(0, len(soup_find_all)):
        soup_item = soup_find_all[i]
        scraped_info = scrapeSoupItem(soup_item)
        if len(scraped_info) == 12:
            scraped_info.insert(2, '999')
        scraped_cleaned = cleanUp(scraped_info)
        writeDict(scraped_cleaned, data_dict, date_string)
    return data_dict

        

