# Vorbereitung
# pip install requests
# pip install beautifulsoup4
# pip install selenium
# edge https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# https://selenium-python.readthedocs.io/getting-started.html
# https://github.com/mozilla/geckodriver/releases

# Module importieren

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import re
import json

class Article:
    def __init__(self):
        self.link = ""
        self.source = "blick.ch"
        self.type = 0
        self.author = ""
        self.published =""
        self.updated = ""
        self.content = ""
        self.fake = 0

def extract(link):
    extractorbrowser = webdriver.Firefox()
    time.sleep(15)
    try:
        extractorbrowser.get(link)
    except TimeoutError:
        time.sleep(200)
        extractorbrowser.get(link)
        exit()
    extractorbrowser.implicitly_wait(20)
    try:
        article = ""
        text=extractorbrowser.find_element(By.CLASS_NAME,'sc-ehof6h-0')
        print(text.text)
        article=rmmorearticles(text.text).replace("WERBUNG",'')
        if article != "":
            articleobject = Article()
            articleobject.link = link
            articleobject.content = (cleanhtml(article))
            exportjson(json.dumps(articleobject.__dict__))
    except NoSuchElementException:
            print("liveticker")
    extractorbrowser.quit()

def rmmorearticles(text):
  where_ellipsis = text.find('Das könnte dich auch interessieren')
  if where_ellipsis == -1:
    return text
  return text[:where_ellipsis]



def exportjson(object):
    with open('blick.json', 'a') as f:
        f.write(object)

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def exportlinks(browser):
    elements = browser.find_elements(By.CLASS_NAME, "yuRUbf")
    for element in elements:
        print(element.find_element(By.TAG_NAME, "a").get_attribute('href'))
        extract(element.find_element(By.TAG_NAME, "a").get_attribute('href'))

browser = webdriver.Firefox()
url = "https://www.google.ch/search?q=site%3Ablick.ch+corona&sxsrf=APq-WBuxA-pdNSraW5hJkTOaw-mE5ESCsg%3A1648015994324&ei=ero6Ys63E8b8kwWbsKSgCw&ved=0ahUKEwjO3LP_ydv2AhVG_qQKHRsYCbQQ4dUDCA4&uact=5&oq=site%3Ablick.ch+corona&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsANKBQg8EgExSgQIQRgASgQIRhgAUABYAGCUA2gBcAF4AIABAIgBAJIBAJgBAMgBB8ABAQ&sclient=gws-wiz"
browser.get(url)
browser.find_element(By.CSS_SELECTOR, "#L2AGLb > div:nth-child(1)").click()
browser.implicitly_wait(20)
print("we need more data")
articles=[]
exportlinks(browser)
nextpage=2
while True:
    try:
        browser.find_element(By.LINK_TEXT, str(nextpage)).click()
        #browser.find_element(By.LINK_TEXT,"2").click()
        print("next page loaded")
        browser.implicitly_wait(40)
        exportlinks(browser)
        time.sleep(2)
        nextpage=nextpage+1
    except NoSuchElementException:
        break

print("loadeddata")

