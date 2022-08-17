#
# Программа получает информацию о предприятиях деревопереробатующего комплекса.
# На alestech.ru/factories получает список областей. Заходим в каждую область и
# получаем всю информацию по каждому предприятию. Все сохраняем в файл excel.
#

import os
import time
import requests
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from saveresult import save_result

# Если получать карточку через requests, то не отлает email (антиспам)
# Пришлось запускать Selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument(r"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
services = Service('chromedriver.exe')
driver = webdriver.Chrome(options=options, service=services)
driver.implicitly_wait(5)
driver.set_page_load_timeout(20)

# получаем ссылки на области
r = requests.get(r'https://alestech.ru/factories')
if r.status_code != 200:
    print('Не могу получить URL https://alestech.ru/factories')
    exit()
soup = bs(r.text, "lxml")
obls = soup.find_all("a", attrs={"class": "red cuprum bold"})

# перебираем все области
for obl in obls:
    otn_path = obl.get("href")
    fl_goto_next_page = True        # флаг захода на страницу
    while fl_goto_next_page:
        # получаем список всех предприятий на странице области
        obl_url = f'https://alestech.ru{otn_path}'
        print(f'*** ОБЛАСТЬ: {obl_url}')
        r = requests.get(obl_url)
        if r.status_code != 200:
            print('Не могу получить URL ' + obl_url)
            exit()
        soup_obl = bs(r.text, "lxml")
        firms = soup_obl.find_all("a", attrs={"class": "text-wrap"})

        # перебираем все предприятия на странице области
        for firm in firms:
            firm_url = f'https://alestech.ru{firm.get("href")}'
            firm_id = firm_url.split("/")[4]
            if not os.path.exists(f"Out\\{firm_id}.txt"):
                # получаем ифу по лпк, если ранее не скачали (файл отсутствует)
                try:
                    driver.get(firm_url)
                    time.sleep(1)
                except:
                    pass
                print(f'Фирма: {firm_id} {firm_url}')
                # разбираем
                soup = bs(driver.page_source, "lxml")
                а_title = soup.find("h3", attrs={"class": "m-0"}).text
                а_desc = soup.find("div", attrs={"class": "mb-3 text-left"})
                а_desc = а_desc.text.replace("\n", " ").replace("\n", " ").strip()
                element = driver.find_element(By.XPATH, value="//div[@class='mb-3 text-left blanks']")
                soup = bs(element.get_attribute('innerHTML'), "lxml")
                а_cont = soup.text
                # сайт организации
                try:
                    а_url = soup.find("a").get("href")
                except:
                    а_url = ''
                # сохраняем
                with open(f"Out\\{firm_id}.txt", "w", encoding="utf8") as f:
                    f.write(а_title + "\n")
                    f.write(а_desc + "\n")
                    f.write(а_cont + "\n")
                    f.write(а_url + "\n")
        try:
            # ищем ссылку на следующую страницу фирм в текущей области
            next_page = soup_obl.find("li", attrs={"class": "d-flex next"})
            otn_path = next_page.find("a", attrs={"class": "my-auto mx-1"}).get("href")
        except:
            # если следующей страницы нет, то переходим к следующей области
            fl_goto_next_page = False

save_result()
print('done.')
