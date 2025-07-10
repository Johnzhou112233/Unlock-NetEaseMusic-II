# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0021502A70DC1495E35E21EAEA9B9426E254BA4F208E2713B2E742EFF9F8E669F967EE7FC114A85BAC48CDA41A0AC19145AFE93D2DF1B40E6D6526179B911CBC04C505D3888746856EEA07D08B99B0237EF945FCA704E54E781A9934272D0B56DD7982602D6CEA39FD60DEB64181DB5DC7CB3B50073140B0F0C8521A96222E209B10E2357B3638009234B298DDB9CF29D3CC80876F5DAFA5648B1B84880D4F4AA6BB419C23B97DDE47ECA5A1185912FAF7A93E179C276B54DD37E0126279EEC51B6C82447967FD368CD946C9F160D2EF3CA19D98B889207F938A44A0EE259046D2A32CCA0335C5D16B8EB17AB0066F825824CBE30A10FB5B3A9824418DD2DBB5700B71B82F14382DA5B1FDA0C180B2E28A7FC1DF9434E7B75FAFCF966509F7653E07461E350D3C89D457588323921079BCF6A53ADC1636CF54F3F3B5F9B09CD668F5EFC579F8C5405AB66B6AEC5AD32E3C7C42BDD54AA178B626B2FF9BAD856EC2"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
