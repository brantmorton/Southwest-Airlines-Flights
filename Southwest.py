

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import csv
import pandas as pd
from search_params import departure_airport, departure_date, return_date
from send_email import send

i = 0
depart_price_list = []
return_price_list = []
destination_list = []

# INITIATING WEB DRIVER TO SWA WEBSITE
driver = webdriver.Chrome()
driver.get("https://www.southwest.com/")
time.sleep(5)


# SETTING DEPARTURE AIRPORT
def departure_airport_filler():
    time.sleep(2)
    departure_fill = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='LandingPageAirSearchForm_originationAirportCode']")))
    departure_fill.send_keys(departure_airport)


def arrival_locations():
    where_we_fly = driver.find_element_by_xpath("//div[@class='modal-trigger']")
    where_we_fly.click()
    driver.implicitly_wait(5)
    list_view = driver.find_element_by_xpath("//button[@aria-controls='air-stations-list']")
    list_view.click()


def get_airports():
    airports = driver.find_elements_by_xpath("//li[@class='air-stations-list--item']")
    airports_trapped_in_parent = driver.find_elements_by_xpath(
        "//li[@class='air-stations-list--item air-stations-list--child-item']")

    for entry in airports:
        destination = entry.text
        if destination not in destination_list:
            destination_list.append(destination)

    for entry in airports_trapped_in_parent:
        destination = entry.text
        if destination not in destination_list:
            destination_list.append(destination)

    close_airport_list()
    return destination_list


def close_airport_list():
    close = driver.find_element_by_xpath('(//button)[17]')
    close.click()


def perform_search():
    city_list = get_airports()
    for city in city_list:
        global i
        i += 1
        city = city[-3:]
        city = city.upper()
        url = f'https://www.southwest.com/air/booking/select.html?int=HOMEQBOMAIR&adultPassengersCount=1&' \
            f'departureDate={departure_date}&departureTimeOfDay=ALL_DAY&destinationAirportCode={city}&fareType=USD&' \
            f'originationAirportCode={departure_airport}&passengerType=ADULT&promoCode=&reset=true&' \
            f'returnDate={return_date}&returnTimeOfDay=ALL_DAY&seniorPassengersCount=0&tripType=roundtrip'

        driver.get(url)
        if i == 1:
            time.sleep(2)
        make_price_list()


def make_price_list():
    there_is_prices = sort_page()
    if there_is_prices:
        depart_price_list.append(get_departing_price())
        return_price_list.append(get_return_price())
    else:
        depart_price_list.append(' ')
        return_price_list.append(' ')


def is_there_departing_fare():
    loop = 0
    while loop < 2:
        try:
            loop += 1
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "(//input[@aria-label='Sort results by'])")))
            flag = True
            break
        except WebDriverException:
            flag = False
            pass
    return flag


def sort_page():
    flag = is_there_departing_fare()
    if flag:
        while True:
            try:
                try:
                    top_sort = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, "(//input[@aria-label='Sort results by'])")))
                    top_sort.click()
                    top_price = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, "(//li[@role='option'])[3]")))
                    top_price.click()
                    break
                except TimeoutException:
                    break
            except WebDriverException:
                pass
    else:
        return False

    try:
        time.sleep(1)
        bottom_sort = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@aria-label='Sort results by'])[2]")))
        bottom_sort.click()
        bottom_price = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "(//li[@role='option'])[3]")))
        bottom_price.click()
    except TimeoutException:
        pass

    return True


def init_csv():
    with open('SW Flights.csv', 'w', newline='') as csvfile:
        fieldnames = ['Departure Airport', 'Destination', 'Departure Price', 'Return Price', 'Total Price', 'Points']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for iterable in range(i):
            try:
                total_price = float(depart_price_list[iterable]) + float(return_price_list[iterable])
                point_total = float(total_price) * 100 / 1.6

            except ValueError:
                total_price = ' '
                point_total = ' '

            if total_price != ' ':
                writer.writerow({'Departure Airport': departure_airport,
                                 'Destination': destination_list[iterable],
                                 'Departure Price': depart_price_list[iterable],
                                 'Return Price': return_price_list[iterable],
                                 'Total Price': total_price,
                                 'Points': point_total})
    csvfile.close()


def get_departing_price():
    try:
        departing_fare = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, "(//span[@class='transition-content'])[2]"
                       "//div[@class='fare-button fare-button_primary-yellow select-detail--fare']")))
        raw_price = departing_fare.get_attribute("innerText")
        departing_price = raw_price.split()[0]

        return departing_price

    except TimeoutException:
        return ' '


def get_return_price():
    try:
        returning_fare = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.XPATH,  "(//span[@class='transition-content'])[4]"
                        "//div[@class='fare-button fare-button_primary-yellow select-detail--fare']")))
        raw_price = returning_fare.get_attribute("innerText")
        returning_price = raw_price.split()[0]

        return returning_price
    except TimeoutException:
        return ' '


def sort_csv():
    df = pd.read_csv('SW Flights.csv')
    sort_by_price = df.sort_values('Total Price')
    sort_by_price.to_csv('SW_Flights_sorted.csv', index=False)


# To send an email with the results, fill out "send_email.py" and uncomment send()
def run_program():
    arrival_locations()
    perform_search()
    init_csv()
    sort_csv()
    driver.close()
    # send()


run_program()
