import os
import requests
import json
import time
import random
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import logging
import re


def call_login_token():
    dict1 = {
        "username": "k.sehat",
        "password": "Ks@123456",
        "applicationType": 961,
        "iP": "1365"
    }
    r = requests.post(url='http://192.168.115.10:8081/api/Authentication/RequestToken',
                      json=dict1,
                      )
    token = json.loads(r.text)['token']
    expire_date = json.loads(r.text)['expires']
    return token, expire_date


def api_token_handler():
    if 'token_expire_date.txt' in os.listdir():
        with open('token_expire_date.txt', 'r') as f:
            te = f.read()
        expire_date = te.split('token:')[0]
        token = te.split('token:')[1]
        if dt.now() >= dt.strptime(expire_date, '%Y-%m-%d'):
            token, expire_date = call_login_token()
            expire_date = expire_date.split('T')[0]
            with open('token_expire_date.txt', 'w') as f:
                f.write(expire_date + 'token:' + token)
    else:
        token, expire_date = call_login_token()
        expire_date = expire_date.split('T')[0]
        with open('token_expire_date.txt', 'w') as f:
            f.write(expire_date + 'token:' + token)
    return token


def click_operation(driver, xpath):
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element.click()
    except:
        click_operation(driver, xpath)


def send_keys_operations(driver, xpath, keys):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
    except:
        send_keys_operations(driver, xpath, keys)


def get_booking_page(data):
    url: str = ("https://www.flygp.se/guru2/v3.5/")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, service=Service(
        "C:\Project\sepehr_scrapper\chromedriver-win64\chromedriver-win64/chromedriver.exe"))
    driver.get(url=url)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[1]/div[2]/input')))
    compBox = driver.find_element(By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[1]/div[2]/input')
    compBox.send_keys('shi')
    loginBox = driver.find_element(By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[2]/div[2]/input')
    loginBox.send_keys('mike.tango')
    passBox = driver.find_element(By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[3]/div[2]/input')
    passBox.send_keys('09125820385')
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div[1]/div/div[2]/button')

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Close")]'))).click()
        # driver.find_element(By.XPATH, '//span[contains(text(), "Close")]').click()
        driver.find_element(By.XPATH, '//span[contains(text(), "Update all")]').click()
    except:
        pass

    try:
        driver.find_element(By.XPATH,
                            '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/div[2]/button[2]/span').click()
        time.sleep(5)
    except:
        pass

    try:
        driver.find_element(By.XPATH, '//span[contains(text(), "Go to update tab")]').click()
    except:
        pass

    try:
        click_operation(driver, '//div[@id="clickDiv"]')
    except:
        pass

    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div/button/span')

    # flight no
    stringBox = driver.find_element(By.XPATH, '//*[@id="flightNo"]')
    stringBox.send_keys(data['flightNo'])
    # flight ADEP
    stringBox = driver.find_element(By.XPATH, '//*[@id="adep"]')
    stringBox.send_keys(data['adep'])
    # flight STD
    stringBox = driver.find_element(By.XPATH, '//*[@id="std"]')
    stringBox.send_keys(data['std'])
    # flight Tail-ID
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div/div[1]/form/div/div[2]/div/div/div')
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["tail_id"]}")]'))).click()
    except:
        return 'Tail_id is not available.'
    # flight ADES
    stringBox = driver.find_element(By.XPATH, '//*[@id="ades"]')
    stringBox.send_keys(data['ades'])
    # flight STA
    stringBox = driver.find_element(By.XPATH, '//*[@id="sta"]')
    stringBox.send_keys(data['sta'])
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div/div[1]/form/div/div[8]/button[2]/span')
    # click use metar
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/label/span[2]')))
    click_operation(driver, '//*[@id="123123"]')
    # driver.find_element(By.XPATH,
    #                     '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/label/span[2]').click()
    # enter mass
    WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mass"]')))
    driver.find_element(By.XPATH, '//*[@id="mass"]').send_keys('0')
    # click Runways tab
    WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[2]/button[2]/span')))
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[2]/button[2]/span')
    # wait untill the results are available
    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH,
         '//p[@class="MuiTypography-root MuiListItemText-secondary MuiTypography-body2 MuiTypography-colorTextSecondary MuiTypography-displayBlock"]')))
    time.sleep(10)
    not_empty = True
    i = 0
    result_list = []
    while not_empty:
        i += 1
        try:
            result_list.append(driver.find_element(By.XPATH,
                                                   f'//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div[2]/nav/div[{i}]').text.split(
                '\n'))
        except Exception as e:
            not_empty = False
            # logger.error(f'Error occured while reading row {i} the table and error is: {e}.')

    result1 = []
    for l in result_list:
        dict1 = {
            "fkFlightInformation": data['fkFlightInformation'],
            "flightNumber": data['flightNo'],
            'bandNumber': l[0],
            'feet': int(l[1].split(' ')[0]),
            'weight': int(l[2].split((' '))[0])
        }
        result1.append(dict1)
    result = {'guruBatchRequestItemViewModels': result1}
    # TODO: the driver wait should be added and the open website should be handled.
    driver.close()
    return result


while True:
    danger_counter = 0
    if (dt.now().hour == 1 and dt.now().minute == 1):
        token = api_token_handler()
        r = requests.get(url='http://192.168.115.10:8081/api/Guru/GetAllFlightsForGuru',
                         headers={'Authorization': f'Bearer {token}',
                                  'Content-type': 'application/json',
                                  })
        data = json.loads(r.content)
        danger_counter = 0
        while not len(data['getAllFlightsForGuruItemsResponseViewModels']) == 0 and danger_counter <= 200:
            danger_counter += 1
            flight = data['getAllFlightsForGuruItemsResponseViewModels'][0]
            try:
                result = get_booking_page(flight)
            except:
                data['getAllFlightsForGuruItemsResponseViewModels'].append(
                    data['getAllFlightsForGuruItemsResponseViewModels'][0])
                data['getAllFlightsForGuruItemsResponseViewModels'].pop(0)
            try:
                r_final = requests.post(url='http://192.168.115.10:8081/api/Guru/CreateGuruBatch',
                                        json=result,
                                        headers={'Authorization': f'Bearer {token}',
                                                 'Content-type': 'application/json',
                                                 })
                if r_final.status_code == 200 and json.loads(r_final.text)['msg'] == 'Records saved successfully ':
                    data['getAllFlightsForGuruItemsResponseViewModels'].pop(0)
                else:
                    data['getAllFlightsForGuruItemsResponseViewModels'].append(
                        data['getAllFlightsForGuruItemsResponseViewModels'][0])
                    data['getAllFlightsForGuruItemsResponseViewModels'].pop(0)
            except:
                print(
                    f'Results for flight fkFlightInformation:{data["fkFlightInformation"]} and flightNumber:{data["flightNo"]} were not imported to database.')
                data['getAllFlightsForGuruItemsResponseViewModels'].append(
                    data['getAllFlightsForGuruItemsResponseViewModels'][0])
                data['getAllFlightsForGuruItemsResponseViewModels'].pop(0)
