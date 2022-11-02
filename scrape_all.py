from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape():
    data = {}
    browser = Browser('chrome', **executable_path, headless=False)
    title, paragraph = news(browser)

    data['title'] = title
    data['paragraph'] = paragraph
    data['image'] = image(browser)
    data['facts'] = facts()
    data['hemispheres'] = hemis(browser)
    
    return data


def news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title,news_p


def image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    return f'https://spaceimages-mars.com/{img_url_rel}'


def facts():
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()


def hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []

    for i in range(4):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a h3')[i].text
        browser.find_by_css('a h3')[i].click()
        hemisphere['image'] = browser.find_by_text('Sample')['href']
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    browser.quit()

    return hemisphere_image_urls
    
