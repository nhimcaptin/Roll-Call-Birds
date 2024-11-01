from selenium import webdriver
import time
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import concurrent.futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
from utils import (
    action_play_game,
    getUserDataDir,
    chrome_driver_path,
    clickButton,
    timesSleep,
    authenticationWallet,
)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("selenium.webdriver").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

countProject = int(input("Nhập số profile: "))
numberThreads = int(input("Nhập số luồng: "))
proxy = []
buttonActions = [
    "//button[@type='button' and contains(text(), 'Continue')]",
    "//img[@alt='hammer']",
    "//a[@href='/daily']",
]


with open("proxy.txt", "r", encoding="utf-8") as file:
    for line in file:
        proxy.append(line.strip())


def run_profile(i):
    user_data_dir = getUserDataDir(i)
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--proxy-server=http://{proxy[i-1]}")
    chrome_options.add_argument("--window-size=250,600")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(1)
    driver.get("https://web.telegram.org/k/#@birdx2_bot")
    time.sleep(2)
    driver.refresh()
    time.sleep(5)
    action_play_game(driver)

    try:
        # Chuyển sang iframe chứa tab
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        for button in buttonActions:
            clickButton(driver, button)

        isCheckExist = clickButton(
            driver,
            "//button[not(contains(@class, 'pointer-events-none')) and contains(., 'Day')]",
            "Đã điểm danh rồi"
        )
        
        if isCheckExist:
            raise
        authenticationWallet(driver)

    except Exception as e:
        pass

    time.sleep(5)
    driver.quit()


with concurrent.futures.ThreadPoolExecutor(max_workers=numberThreads) as executor:
    executor.map(run_profile, range(1, countProject + 1))
