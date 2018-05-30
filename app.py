
# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
from flask import render_template, redirect
from flask import Flask
app = Flask(__name__)
import requests

# Initialize PyMongo to work with MongoDBs
client = pymongo.MongoClient('localhost', 27017)
db = client['mars_database']

#app route to scrape
@app.route('/scrape')
def scrape():
    # putting executable_path
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # url for mars nasa website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # initilize browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
   
    #getting header and paragraf data
    header = soup.find('div', class_='content_title')
    paragraf = soup.find('div', class_='article_teaser_body')
   
    #striping the texts
    news_title = header.text.strip()
    news_p = paragraf.text.strip()

    # url to get images from a website
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # getting images urls
    image = soup.find_all('div', class_='img')
    url = image[0].img["src"]

    # creating url feastured url
    featured_image_url = ['https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + url]

    # url for twitter to get weather data
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = results = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    # the most recent mars weather data
    mars_weather = mars_weather = results.text.strip()

    #url to space facts website
    url = 'http://space-facts.com/mars/'

    # getting data to a table 
    tables = pd.read_html(url)

    # putting data in pandas data frame and then expoting to html file
    df = tables[0]
    df = df.rename({0: 'Planet Data Type', 1: 'Value'}, axis=1).set_index('Planet Data Type')
    df.to_html("mars_information_table.html")

    # configuring html table 
    html_table = df.to_html(index=False)
    html_table = html_table.replace('\n', '')

    #url to astrogeology website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # getiing url information to get images
    mars_items = soup.find_all(class_="item")
    url_list = []
    titles =[]
    hemisphere_image_urls =[]

    # for loop to get all titles and urls
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

        #putting data in to a list
        hemisphere_image_urls.append(post)

    # creating a dictionary which contain all of the data
    all_data_from_scrape = {
        "list_of_hemisphere_image_urls": hemisphere_image_urls,
        "Mars_weather": mars_weather,
        "Html_table": html_table,
        "News_title":news_title,
        "News_p":news_p
    }
    # droping the collection to clear previous records
    db.posts.drop()
    #inserting the dictionary to our database
    db['posts'].insert(all_data_from_scrape)
    # return to the index route after scrape been completed
    return redirect("http://localhost:5000/", code=302)

@app.route('/', methods=['POST','GET'])
def getData():
    #getting data from the database by using mongodb
    data = db.posts.find()[0]
    #render index.html
    return render_template('index.html', mars=data)
#run the app
if __name__ == '__main__':
    app.run(debug=True)

