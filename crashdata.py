import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os

driver = None
firstRound = True
crashes_num = 1

if os.path.isfile("crash_data.csv"):
    crashdata = pd.DataFrame(columns=["All Crashes"])
else:
    # creates new file if it doesn't exist
    crashdata = pd.DataFrame(columns=["All Crashes"])
    crashdata.to_csv('crash_data.csv', mode='w', index=False)


def check_round():
    global firstRound
    while True:
        if pyautogui.locateOnScreen("preparing_round.png", confidence=0.8) is not None:
            grab_first_number()
            time.sleep(6)
        # enable if you want it to skip the first round, but delete/comment out the statement above
        """
        if pyautogui.locateOnScreen("preparing_round.png", confidence=0.8) is not None and firstRound is False:
            grab_first_number()
            time.sleep(6)
        elif pyautogui.locateOnScreen("preparing_round.png", confidence=0.8) is not None and firstRound is True:
            firstRound = False
            time.sleep(6)"""
        time.sleep(0.1)


def grab_first_number():
    global driver, crashdata, crashes_num
    values = driver.find_elements(By.CLASS_NAME, "MuiButton-label")
    nextIsNumber = False

    for i in values:
        if i.text == "Play Demo":
            nextIsNumber = True
        elif nextIsNumber:
            num = float(str(i.text).split("x")[0])
            nextIsNumber = False

            # append it to the csv file
            crashdata.loc[0] = [num]
            crashdata.to_csv('crash_data.csv', mode='a', header=False, index=False)
            crashdata = pd.DataFrame(columns=["All Crashes"])
            print(str(num) + "    #" + str(crashes_num))
            crashes_num += 1


def load_page():
    global driver
    link = "https://roobet.com/crash"
    # installs local chromes supported driver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(link)
    except:
        pass


def run():
    load_page()
    while True:
        check_round()


run()
