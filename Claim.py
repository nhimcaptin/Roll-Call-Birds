from selenium import webdriver
import time
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import concurrent.futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import action_play_game, getUserDataDir, chrome_driver_path, clickButton, timesSleep, getInformationWorm, allActionWorm, authenticationWallet

countProject = int(input("Nhập số profile: "))
numberThreads = int(input("Nhập số luồng: "))
proxy = []
buttonActions = [
    "//button[@type='button' and contains(text(), 'Continue')]",
    "//div[@class='absolute flex text-center justify-center flex-col -top-3.5 items-center']/p",
]

buttonInformation = [
    ['//div[@class="flex flex-col items-center cursor-pointer gap-1 bg-black/50 px-2 rounded-md"]//p[text()="5"]',
     '//div[@class="flex flex-col items-center cursor-pointer gap-1 bg-black/50 px-2 rounded-md"]//p[text()="5"]/following::p[1]',
     '//div[p[text()="5"] and img]'],
    ['//div[@class="flex flex-col items-center cursor-pointer gap-1 bg-black/50 px-2 rounded-md"]//p[text()="20"]',
     '//div[@class="flex flex-col items-center cursor-pointer gap-1 bg-black/50 px-2 rounded-md"]//p[text()="20"]/following::p[1]',
     '//div[p[text()="20"] and img]'],
    ['//div[@class="flex flex-col items-center gap-1 bg-black/50 px-2 rounded-md"]//p[text()="60"]',
     '//div[@class="flex flex-col items-center gap-1 bg-black/50 px-2 rounded-md"]//p[text()="60"]/following::p[1]',
     '//div[p[text()="60"] and img]'],
]


with open("proxy.txt", "r", encoding="utf-8") as file:
    for line in file:
        proxy.append(line.strip())


def run_profile(i):
    user_data_dir = getUserDataDir(i)
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--proxy-server=http://{proxy[i-1]}")
    chrome_options.add_argument("--window-size=250,1000")

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
            
        try: 
            buttonApprove = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Claim rewards']"))
            )
            buttonApprove.click()
        except Exception as e:
            value_element = driver.find_element(By.XPATH, '//div[@class="flex items-center justify-between mb-1 text-sm"]/p')
            value = value_element.text.split("/")
            currentPoints = int(value[0])
            totalPoints = int(value[1])
            informationWorm = getInformationWorm(driver, buttonInformation)
            _allActionWorm =  allActionWorm(totalPoints - currentPoints, informationWorm)
            
            for actionWorm in _allActionWorm:
                print("actionWorm", actionWorm)
                clickButton(driver, "//div[p[text()='5'] and img]")
                # authenticationWallet(driver)
            # buttonStartPery = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[text()='Start Preying']"))
            # )
            # buttonStartPery.click()
            
            
        # authenticationWallet()
    except Exception as e:
        print(f"Không thể click vào tab 'Earn': {e}")

    time.sleep(5)
    driver.quit()


with concurrent.futures.ThreadPoolExecutor(max_workers=numberThreads) as executor:
    executor.map(run_profile, range(1, countProject + 1))
