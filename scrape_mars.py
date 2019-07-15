#import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser

def init_browser():
    #set up splinter to use Chrome
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()
    facts = {}

    #visit nasa page with splinter
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    nasa_title = soup.find('div', class_='content_title').text
    nasa_news = soup.find('div', class_='article_teaser_body').text

    #visit JPL website with splinter|
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    #use Beautiful Soup to collect url of featured image
    html = browser.html
    soup = bs(html, 'html.parser')

    jpl_featured_url = soup.find('article', class_='carousel_item')
    jpl_featured_url = jpl_featured_url.find(id="full_image")
    jpl_featured_url = jpl_featured_url.attrs['data-fancybox-href']
    jpl_featured_url = 'https://www.jpl.nasa.gov' + jpl_featured_url

    #visit Mars Weather twitter page with splinter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #use Beautiful Soup to collect text of most recent tweet
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    #get Mars Facts
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    df = table[0]
    df.set_index('Mars - Earth Comparison', inplace=True)
    df = df.iloc[1:]
    table = print(df)



    #visit astrology.usgs.gov with splinter
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #get links to each hemisphere
    html = browser.html
    soup = bs(html, 'html.parser')
    base_url = 'https://astrogeology.usgs.gov/'

    mars_hemispheres = soup.find_all('a', class_='itemLink product-item')
    hemisphere1 = base_url + mars_hemispheres[0].attrs['href']
    hemisphere2 = base_url + mars_hemispheres[2].attrs['href']
    hemisphere3 = base_url + mars_hemispheres[4].attrs['href']
    hemisphere4 = base_url + mars_hemispheres[6].attrs['href']

    #Visit each link, collect hemisphere name and URL of image
    browser.visit(hemisphere1)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere1 = soup.find_all('li')
    hemisphere1_link = hemisphere1[0].find().attrs['href']
    hemisphere1_name = hemisphere1_link[61:]
    hemisphere1_name = hemisphere1_name[:-22]
    hemisphere1_name = hemisphere1_name.title()
    hemisphere1_name = hemisphere1_name.replace('_',' ')


    browser.visit(hemisphere2)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere2 = soup.find_all('li')
    hemisphere2_link = hemisphere2[0].find().attrs['href']
    hemisphere2_name = hemisphere2_link[61:]
    hemisphere2_name = hemisphere2_name[:-22]
    hemisphere2_name = hemisphere2_name.title()
    hemisphere2_name = hemisphere2_name.replace('_',' ')


    browser.visit(hemisphere3)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere3 = soup.find_all('li')
    hemisphere3_link = hemisphere3[0].find().attrs['href']
    hemisphere3_name = hemisphere3_link[61:]
    hemisphere3_name = hemisphere3_name[:-22]
    hemisphere3_name = hemisphere3_name.title()
    hemisphere3_name = hemisphere3_name.replace('_',' ')


    browser.visit(hemisphere4)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere4 = soup.find_all('li')
    hemisphere4_link = hemisphere4[0].find().attrs['href']
    hemisphere4_name = hemisphere4_link[61:]
    hemisphere4_name = hemisphere4_name[:-22]
    hemisphere4_name = hemisphere4_name.title()
    hemisphere4_name = hemisphere4_name.replace('_',' ')


    facts['nasa_title'] = nasa_title
    facts['nasa_news'] = nasa_news
    facts['jpl_featured_url'] = jpl_featured_url
    facts['mars_weather'] = mars_weather
    facts['mars_facts'] = table
    facts['hemisphere1_name'] = hemisphere1_name
    facts['hemisphere1_link'] = hemisphere1_link
    facts['hemisphere2_name'] = hemisphere2_name
    facts['hemisphere2_link'] = hemisphere2_link
    facts['hemisphere3_name'] = hemisphere3_name
    facts['hemisphere3_link'] = hemisphere3_link
    facts['hemisphere4_name'] = hemisphere4_name
    facts['hemisphere4_link'] = hemisphere4_link

    return facts