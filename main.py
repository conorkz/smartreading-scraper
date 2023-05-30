from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import os
directory =  r"your_directory"
roi = 'no info on the website'
s = Service("PATH_TO_CHROMEDRIVER")
driver = webdriver.Chrome(service=s)
driver.get('https://smartreading.ru/user-unauthorized-message')
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, '.btn.btn--primary.btn--lg.w--full').click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, '[name=email]').send_keys('YOUR_LOGIN')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[name=password]').send_keys('YOUR_PASSWORD')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
time.sleep(5)
x = 1
while True:
    if x == 1004:
        break
    link = f'https://smartreading.ru/summary/{x}/epub/read'
    driver.get(link)
    print(link)
    WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.fixed-holder')))
    time.sleep(12)
    x+=1
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if soup.select_one('.error-404--image'):
        continue
    title = soup.find('h1', style='text-align: left;').text
    author = soup.find('h1', style='text-align: left;').find_next().text.replace('Автор:', '').strip()
    current_time = datetime.now(pytz.timezone('Europe/Berlin'))
    berlin = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    bf = re.sub(r"[^\w\s]", "", title)
    file_name = os.path.join(directory, f"{bf}.txt")
    suffix = 1
    while os.path.exists(file_name):
        file_name = os.path.join(directory, f"{bf} ({suffix}).txt")
        suffix += 1
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Link: {link}\n")
        file.write(f"Title: {title}\n")
        file.write(f"Author: {author}\n")
        file.write(f"Berlin time: {berlin}\n\n")
        for s in soup.find(id='epub-reader-inner-box').find_all(['h3', 'p', 'li']):
            file.write(s.text + '\n\n')
        