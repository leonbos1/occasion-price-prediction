import selenium
from selenium import webdriver
import time
from models.car import Car
import csv
import os
import json

cookie_compliance = {
    "name": "as24-cmp-signature",
    "value": "mQU3gwNjz4b4ZIkng8cjoMSfYl0tr6C6rjGRD3bQ8OsvzRCsdTwdANA8q9CBpJFSImfd9%2F7V9E9wFJ03A2yCxM%2B1rpGv%2BxZB7lAkvN3zOp9oK7aYi%2B%2FHf9LvZD2II81gqcWJFemzUYPcvLiTxkHidoC%2Fwh1La12ZDuGUXiIDPmE%3D"
}


def scrape(brand: str = None, model: str = None):
    driver = webdriver.Firefox()
    time.sleep(1)

    driver.get('https://www.autoscout24.nl/')

    click_cookies(driver)

    brand = brand.replace(' ', '-').lower()

    if brand and model:
        urls = [f'https://www.autoscout24.nl/lst/{brand}/{model}']

    else:
        urls = get_urls()

    for url in urls:

        driver.get(url)

        time.sleep(1)

        article_class = 'cldt-summary-full-item listing-impressions-tracking list-page-item false ListItem_article__ppamD'

        time.sleep(1)

        cars = []

        for i in range(10):

            articles = driver.find_elements_by_xpath(
                f"//article[@class='{article_class}']")

            for article in articles:
                brand = article.get_attribute('data-make')
                model = article.get_attribute('data-model')
                price = article.get_attribute('data-price')
                mileage = article.get_attribute('data-mileage')
                year = article.get_attribute('data-first-registration')
                year = year.split('-')[1]

                try:
                    power_div = "VehicleDetailTable_container__mUUbY"
                    power_span = "VehicleDetailTable_item__koEV4"

                    power = article.find_elements_by_xpath(
                        f"//div[@class='{power_div}']//span[@class='{power_span}']")

                    raw_power = power[4].text

                    power_pk = raw_power.split(' ')[2]
                    power = int(power_pk.replace('(', ''))

                except:
                    power = 0

                car = Car(brand=brand, model=model, buildyear=year,
                          mileage=mileage, price=price, power=power)

                cars.append(car)

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(2)

            next_page_class = 'FilteredListPagination_button__41hHM'
            contains_text = 'Volgende'

            # get element with classname next_page_class and text contains contains_text

            try:
                next_page = driver.find_element_by_xpath(
                f"//button[@class='{next_page_class}' and contains(text(), '{contains_text}')]")

                next_page.click()
            except:
                continue

            time.sleep(1)

        write_to_csv(cars)

    driver.close()


def write_to_csv(cars):
    """Append cars to csv file
    """
    for car in cars:
        brand = car.brand
        model = car.model

        csv_file = f'{brand}_{model}.csv'
        csv_file = os.path.join('cars', csv_file)

        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([car.buildyear, car.mileage, car.price, car.power])


def click_cookies(driver: webdriver):
    cookies = '_consent-accept_1i5cd_111'

    driver.find_element_by_class_name(cookies).click()


def get_urls():
    file = open('cars.json', 'r')

    cars = json.load(file)

    urls = []

    for car in cars:
        for brand in car:
            for model in car[brand]['models']:
                url = f'https://www.autoscout24.nl/lst/{brand}/{model}'
                urls.append(url)

    return urls

if __name__ == "__main__":
    scrape()
