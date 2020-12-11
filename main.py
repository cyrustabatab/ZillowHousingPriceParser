from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import lxml
import time


driver_path = "C:\Development\chromedriver.exe"

google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLScuqpzyGO0LcZ5vAoNjiybOVg_VLj5RdIMjPJRYN38QW3ykxA/viewform?usp=sf_link"

zillow_url = "https://www.zillow.com/san-francisco-ca/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.51174330420326%2C%22east%22%3A-122.35960603051353%2C%22south%22%3A37.74054651440494%2C%22north%22%3A37.829755795772805%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A916671%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D"


headers = {"Accept-Language": 'en-US,en;q=0.9',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55"}

response = requests.get(zillow_url,headers=headers)


soup = BeautifulSoup(response.text,"lxml")
#print(soup.prettify())


links = soup.select(".list-card-top a")

property_links = []
for link in links:
    property_link = link['href']
    if not property_link.startswith('https'):
        property_link = "https://zillow.com" + property_link
    property_links.append(property_link)




addresses = soup.find_all("address",class_="list-card-addr")
prices = soup.select("div.list-card-heading")


def parse_price(price):

    i = 1
    number = [] 
    while price[i].isdigit() or price[i] == ',':
        if price[i].isdigit():
            number.append(price[i])
        i += 1


    return float(''.join(number))




driver = webdriver.Chrome(driver_path)


for link,address,price in zip(property_links,addresses,prices):
    driver.get(google_form_url)
    price = parse_price(price.getText())
    input_1 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_2 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_3 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inputs = [input_1,input_2,input_3]
    values = [address.getText(),price,link]
    for input_entry,value in zip(inputs,values):
        input_entry.send_keys(str(value))

    
    submit_link = driver.find_element_by_class_name('freebirdFormviewerViewNavigationSubmitButton')
    submit_link.click()
    














