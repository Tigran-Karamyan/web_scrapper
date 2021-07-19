# for web_scrapping selenium, bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re


PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://auto.am/search/passenger-cars?q={%22category%22:%221%22,%22page%22:%221%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{%22dealer%22:%220%22,%22id%22:%22%22},%22make%22:[%22386%22],%22year%22:{%22gt%22:%221911%22,%22lt%22:%222022%22},%22usdprice%22:{%22gt%22:%220%22,%22lt%22:%22100000000%22},%22mileage%22:{%22gt%22:%2210%22,%22lt%22:%221000000%22}}")


cars = list() #List to store name of the cars
prices = list() #List to store name of the prices
content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll('a'):
    car = a.find('span', attrs={'class':'card-title bold'})
    price = a.find('div', attrs={'class':'ad-mob-price bold grey-text'})
    if price is not None:
        cars.append(car.text)
        prices.append(price.text)

# Preprocess car names
cars_list = [car.split() for car in cars]
df = pd.DataFrame(cars_list, columns=['Year', 'Mark', 'Model', 'Series', 'Ext'])

full_series = [series + " " + ext 
               if series is not None 
               and ext is not None 
               else series 
               for series, ext in zip(df.Series, df.Ext)]
    
df['Series'] = full_series

full_model = [model + " " + series 
               if model is not None 
               and series is not None 
               else model 
               for model, series in zip(df.Model, df.Series)]
    
df['Model'] = full_model

df.drop(['Series', 'Ext'], axis=1, inplace = True)

# Preprocess prices
prices = [price.replace('$','') for price in prices]

prices = [re.sub('\s', '', price) for price in prices]

prices = [int(price) if price != 'Պայմ.' else 0 for price in prices]

df['Prices'] = prices

df.to_csv("auto.am")
