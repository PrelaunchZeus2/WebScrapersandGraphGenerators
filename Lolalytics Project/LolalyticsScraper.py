#This script is going to comb the lolalytics site to find champion winrate and playrate data for the current patch. Then generate a graph of the data with x as the pickrate and y as the win delta
#The data will be saved in a csv file called Lolalytics_Scraped_Data.csv

#imports
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time




#Site Url
url = 'https://lolalytics.com/lol/tierlist/'

#The site uses lazy loading so we need to scroll down to get all the data
driver = webdriver.Firefox()
driver.get(url)
body = driver.find_element(By.CSS_SELECTOR, 'body')
for _ in range(5):  # Adjust this range according to your needs
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)  # Wait for the page to load


#parse the page
soup = BeautifulSoup(driver.page_source, 'html.parser')
with open('Lolalytics.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
driver.quit()

#get the data
rows = soup.find_all('div', class_='flex h-[52px] justify-between text-[13px] text-[#ccc] odd:bg-[#181818] even:bg-[#101010]')

data = []
for row in rows:
    Rank = row.find(attrs={"q:key": "0"}).text
    Icon = row.find(attrs={"q:key": "0"}).text
    Name = row.find(attrs={"q:key": "SO_0"}).text
    Tier = row.find(attrs={"q:key": "3"}).text
    Lane_pos = row.find(attrs={"q:key": "kS_0"}).get('alt')
    Lane_percent = row.find(attrs={"q:key": "SO_4"}).text
    Win = row.find(attrs={"q:key": "Ts_0"}).text
    Pick = row.find(attrs={"q:key": "6"}).text
    Ban = row.find(attrs={"q:key": "7"}).text
    Pbi = row.find(attrs={"q:key": "8"}).text
    Games = row.find(attrs={"q:key": "9"}).text.strip().replace(',', '')
    data.append([int(Rank), str(Name), str(Tier), str(Lane_pos), str(Lane_percent), float(Win), float(Pick), float(Ban), int(Pbi), int(Games)])


with open('Lolalytics_Scraped_Data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Name", "Tier", "Lane Position", "Lane Percentage", "Win", "Pick", "Ban", "Pbi", "Games"])
    writer.writerows(data)










 