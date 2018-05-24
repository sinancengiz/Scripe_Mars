import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pymongo


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
!which chromedriver


executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

header = soup.find_all('div', class_='content_title')
paragraf = soup.find_all('div', class_='article_teaser_body')

print(paragraf[0].text)


news_title = header[0].text
news_p = paragraf[0].text


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

image = soup.find_all('div', class_='img')
featured_image_url = image[0].img['src']


url = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


results = soup.find_all('div', class_="js-tweet-text-container")


mars_weather = results[0].p.text



url = 'http://space-facts.com/mars/'

tables = pd.read_html(url)


df = tables[0]
df.columns = ['Planet Data Type', 'Value']
df.set_index('Planet Data Type', inplace=True)



html_table = df.to_html(index=False)
html_table.replace('\n', '')
df.to_html('table.html')



url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# Define database and collection
db = client.craigslist_db
collection = db.items


# URL of page to be scraped
url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


mars_container = soup.find_all('div', class_='container')
mars_image = mars_container[0].find_all('div', class_='downloads')
img_url = mars_image[0].a["href"]


contents = mars_container[0].find_all('div', class_='content')
title = contents[0].h2.text
print(title2)


for container in mars_container:
    # Error handling
    try:
        # Identify and return title of listing
        contents = container.find_all('div', class_='content')
        title = contents[0].h2.text
         # Identify and return link to listing
        img_url = container.find_all('div', class_='downloads')
        img_url = mars_image[0].a["href"]

        # Run only if title, price, and link are available
        if (title and img_url):
            # Print results
            print('-------------')
            print(title)
            print(img_url)
        
           # Dictionary to be inserted as a MongoDB document
            hemisphere_image_urls = {
                'title': title,
                'img_url': img_url
              }

            collection.insert_one(hemisphere_image_urls)

    except Exception as e:
        print(e)
        
    browser.click_link_by_partial_text('next')
