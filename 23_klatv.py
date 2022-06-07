# Vorbereitung
# pip install requests
# pip install beautifulsoup4
# pip install selenium
# edge https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# https://selenium-python.readthedocs.io/getting-started.html
# https://github.com/mozilla/geckodriver/releases


from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import json
from selenium.webdriver.common.action_chains import ActionChains

class Article:
    def __init__(self):
        self.link = ""
        self.source = "kla.tv"
        self.type = 3
        self.author = ""
        self.published =""
        self.updated = ""
        self.content = ""
        self.fake = 1

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
        try:
            extractorbrowser.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/button").click()
        except Exception:
            print("nocoockie")
        extractorbrowser.find_element(By.CSS_SELECTOR, '#vidtab_readmore_tag').click()
        time.sleep(20)
        extractorbrowser.implicitly_wait(20)
        text=extractorbrowser.find_element(By.CLASS_NAME,'comment-content')
        print(text.text)
        article=rmmorearticles(text.text)
        if article != "":
            articleobject = Article()
            articleobject.link = link
            articleobject.content = (cleanhtml(article))
            #articleobject.published = cleanhtml(str(html.find_elements('span', class_="watson-snippet__shareBubbles__published")))
            #articleobject.updated = cleanhtml(str(html.find_elements('span', class_="watson-snippet__shareBubbles__updated")))
            #articleobject.author = cleanhtml(str(html.find_elements('div', class_="watson-snippet__authorbox")))
            exportjson(json.dumps(articleobject.__dict__))
    except Exception:
            print("liveticker")
    extractorbrowser.quit()

def rmmorearticles(text):
  where_ellipsis = text.find('Quellen/Links:')
  if where_ellipsis == -1:
    return text
  return text[:where_ellipsis]



def exportjson(object):
    with open('klatv.json', 'a') as f:
        f.write(object)

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def exportlinks(browser):
    elements=browser.find_elements(By.CLASS_NAME,
                          "searchViewLinksStyle")
    #elements = browser.find_elements(By.CLASS_NAME, "yuRUbf")
    i=0
    for element in elements:
        print(i,"/",elements.__len__())
        print(element.get_attribute('href'))
        extract(element.get_attribute('href'))
        i=i+1


browser = webdriver.Firefox()
url = "https://www.kla.tv/de"
browser.get(url)
browser.implicitly_wait(20)
browser.find_element(By.CSS_SELECTOR, '.btn_trend_white').click()
browser.find_element(By.CSS_SELECTOR, '.vue-autosearch-input').send_keys("corona")
browser.find_element(By.CSS_SELECTOR, '.vue-autosearch-input').send_keys(Keys.RETURN)
print("we need more data")
time.sleep(20)
#newsletter muss manuell wegedrückt werden
while True:
    try:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next=browser.find_element(By.CSS_SELECTOR,'#darkblue_gradient_container > div > div.ng-scope > div.top10_first_item.mt-4 > a')
        ActionChains(browser).click(next).perform()
        #browser.find_element(By.LINK_TEXT,"2").click()
        print("next page loaded")
        browser.implicitly_wait(40)
        time.sleep(10)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception:
        break

print("loadeddata")
exportlinks(browser)
