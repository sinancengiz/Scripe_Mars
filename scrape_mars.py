
# coding: utf-8

# In[152]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
from flask import render_template
from flask import Flask
app = Flask(__name__)
import requests

# Initialize PyMongo to work with MongoDBs
client = pymongo.MongoClient('localhost', 27017)
db = client['mars_database']

@app.route('/scrape')
def scrape():

    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html

    # In[154]:
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # executable_path = {'executable_path': 'chromedriver'}
    # driver = webdriver.Chrome("C:\Users\sinancengiz\Downloads\sinan.zip\sinan\chromedriver.exe")
    # browser = Browser('chrome', **executable_path)


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    header = soup.find('div', class_='content_title')
    paragraf = soup.find('div', class_='article_teaser_body')

    news_title = header.text.strip()
    news_p = paragraf.text.strip()


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    image = soup.find_all('div', class_='img')
    url = image[0].img["src"]

    featured_image_url = ['https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + url]



    # response = requests.get(featured_image_url, stream=True)
    # with open('img.png', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)


    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = results = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_weather = mars_weather = results.text.strip()

    url = 'http://space-facts.com/mars/'

    tables = pd.read_html(url)

    df = tables[0]
    df = df.rename({0: 'Planet Data Type', 1: 'Value'}, axis=1).set_index('Planet Data Type')
    df.to_html("mars_information_table.html")

    html_table = df.to_html(index=False)
    html_table = html_table.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    mars_items = soup.find_all(class_="item")
    url_list = []
    titles =[]
    hemisphere_image_urls =[]

    for item in mars_items:
        title = item.div.h3.text
        titles.append(title)
        link = item.a["href"]
        link = 'https://astrogeology.usgs.gov' + link
    
        # The images are in another link. You need to collect the second link as well. 
        # The second has the image in high resolution
        response_two = requests.get(link)
        
        soup_two = BeautifulSoup(response_two.text, 'html.parser')
        div = soup_two.find('div', class_='downloads')
        image_link = div.a['href']
        url_list.append(image_link)
        post = {
            "title": title,
            "img_url": image_link,
        }
        hemisphere_image_urls.append(post)

    all_data_from_scrape = {
        "list_of_hemisphere_image_urls": hemisphere_image_urls,
        "Mars_weather": mars_weather,
        "Html_table": html_table,
        "News_title":news_title,
        "News_p":news_p
    }
    db['posts'].insert(all_data_from_scrape)
    return all_data_from_scrape

@app.route('/', methods=['POST','GET'])
def getData():
    
    data = db.posts.find()[0]
    
    return render_template('index.html', mars=data)

if __name__ == '__main__':
    app.run(debug=True)

