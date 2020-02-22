# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
from flask import render_template, redirect
from flask import Flask
import requests
import time as time

def scripe_func():
    # putting executable_path
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # url for mars nasa website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(4)
    # initilize browser
    html = browser.html
    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(2)
    #getting header and paragraf data
    header = soup.find('div', class_='content_title')
    paragraf = soup.find('div', class_='article_teaser_body')
    time.sleep(2)
    #striping the texts
    news_title = header.text.strip()
    news_p = paragraf.text.strip()

    # url to get images from a website
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # getting images urls
    # image = soup.find_all('a', class_='button fancybox')
    # featured_image = image[0]["data-fancybox-href"]
    browser.find_by_id("full_image").click()
    time.sleep(4)
    browser.find_link_by_partial_text("more info").click()
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    featured_image = soup.find("figure", class_="lede").find("img")["src"]

    # creating url feastured url
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image

    # url for twitter to get weather data
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(4)
    #browser.find_link_by_partial_text("MarsWxReport").click()
    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    span = results[0].find('span')
    # the most recent mars weather data
    mars_weather = span.text.strip()

    #url to space facts website
    url = 'http://space-facts.com/mars/'

    # getting data to a table 
    tables = pd.read_html(url)[0]

    # putting data in pandas data frame and then expoting to html file

    df = tables.rename({0: 'Planet Data Type', 1: 'Value'}, axis=1).set_index('Planet Data Type')
    # df.to_html("mars_information_table.html")

    # configuring html table 
    html_table = df.to_html()
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
    "News_p":news_p,
    "Featured_image_url":featured_image_url  
    }
    browser.quit()

    return all_data_from_scrape


