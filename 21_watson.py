# Vorbereitung
# pip install requests
# pip install beautifulsoup4
# pip install selenium
# edge https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# https://selenium-python.readthedocs.io/getting-started.html
# https://github.com/mozilla/geckodriver/releases

# Module importieren

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import re
import json

class Article:
    def __init__(self):
        self.link = ""
        self.source = ""
        self.type = ""
        self.author = ""
        self.published =""
        self.updated = ""
        self.content = ""
        self.fake = ""

def extract(link):
    extractorbrowser = webdriver.Firefox()
    time.sleep(15)
    try:
        extractorbrowser.get(link)
    except TimeoutError:
        time.sleep(300)
        extractorbrowser.get(link)
        exit()
    extractorbrowser.implicitly_wait(20)
    response = extractorbrowser.page_source
    html = BeautifulSoup(response, 'html.parser')
    text = html.find_all('p', class_="watson-snippet__text")
    time.sleep(15)
    article = ""
    for parts in text:
        article += str(parts)
    if article != "":
        articleobject = Article()
        articleobject.link = link
        articleobject.source = "Watson"
        articleobject.content = (cleanhtml(article))
        exportjson(json.dumps(articleobject.__dict__))
    extractorbrowser.quit()


def exportjson(object):
    with open('data.json', 'a') as f:
        f.write(object)

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


browser = webdriver.Firefox()
url = "https://www.watson.ch/u/search?q=corona"
browser.get(url)
browser.implicitly_wait(20)
print("we need more data")

while True:
    try:
        print("we need to laod more data")
        # browser.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[2]/div[3]/a").click()
        element = browser.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[2]/div[3]/a")
        browser.execute_script("arguments[0].click();", element)
        print("next page loaded")
        browser.implicitly_wait(40)
        time.sleep(2)
    except NoSuchElementException:
        break

print("loadeddata")
articles = browser.find_elements(By.CLASS_NAME, "storylink")
i = 0
for article in articles:
    print(i,"/",articles.__len__())
    extract(article.get_attribute('href'))
    i=i+1
