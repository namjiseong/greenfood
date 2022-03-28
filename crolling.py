from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from urllib.request import Request, urlopen
import urllib.request
import os

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
elem = driver.find_element_by_name("q")
name = '돈가스'
if not os.path.exists(name):
    os.makedirs(name)

elem.send_keys(name)
elem.send_keys(Keys.RETURN)





SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height


images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 1
for image in images:
    # try:
    image.click()
    time.sleep(2)
    imgUrl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
    
    
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    
    
    
    output_path = './' + name +'/'
    
    urllib.request.urlretrieve(imgUrl, output_path + str(count) + ".jpg")
    
    count = count + 1
    if count > 5:
        break
    # except:
    #     pass

driver.close()