import requests
import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from usernames.usernamegenerator import generate
from mail import MailTM

def create(username:str, name:str, password:str):
    mtm = MailTM(username=username, password=password)
    address = mtm.create()

    op = webdriver.ChromeOptions()
    #op.add_argument('--headless') email_confirmation_code
    op.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    actions = ActionChains(driver)

    driver.get("https://www.instagram.com/accounts/emailsignup/")
    

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'))).click()

    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'emailOrPhone'))).click()
    actions.send_keys(f"{address}").perform()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password'))).click()
    actions.send_keys(f"{password}").perform()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'username'))).click()
    actions.send_keys(f"{username}").perform()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'fullName'))).click()
    actions.send_keys(f"{name}").perform()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/button'))).click()

    time.sleep(1)

    Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//select[@title="Month:"]')))).select_by_value(str(random.choice(list(range(1,12)))))
    Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//select[@title="Day:"]')))).select_by_value(str(random.choice(list(range(1,28)))))
    Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//select[@title="Year:"]')))).select_by_value(str(random.choice(list(range(1980, 2002)))))

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div/div[6]/button'))).click()

    code = None

    while code == None:
        mail = mtm.checkMailbox()
        for i in mail["hydra:member"]:
            subj:str = i["subject"]
            if "is your Instagram code" in subj:
                subjsplit = subj.split()
                code = subjsplit[0]
        time.sleep(5)

    print(code)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'email_confirmation_code'))).click()
    actions.send_keys(f"{code}").perform()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/button'))).click()

