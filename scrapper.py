from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import requests
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("C:/Users/admin/Downloads/Code_Projects/PRO-127/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers = ["name","distance","mass","radius","hyperlink","star","consellation","right_ascension","declination"]
star_data=[]
new_star_data=[]
def scrape():
    for i in range(0,428):
        soup=BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find.all("ul", attrs={"class","star"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index, li_tag in enumerate(li_tags):
                if index ==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                    except:
                           temp_list.append(li_tag.contents[0])
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            star_data.append(temp_list)
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table')

        with open("scrapper2.csv","w") as f:
            csvwriter= csv.writer(f)
            csvwriter.writerrow(headers)
            csvwriter.writerows(star_data)     
def scrape_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup=BeautifulSoup(page.content,"html.parser")
    for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list=[]
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        new_star_data.append(temp_list)

scrape()
for data in star_data:
    scrape_more_data(data[5])

final_star_data=[]

for index, data in enumerate(star_data):
    final_star_data.append(data + final_star_data[index])

with open("final.csv","w") as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_star_data)