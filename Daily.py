from selenium import webdriver
import time
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import concurrent.futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import action_play_game, getUserDataDir, chrome_driver_path, clickButton, timesSleep

countProject = int(input("Nhập số profile: "))
numberThreads = int(input("Nhập số luồng: "))
proxy = []
buttonActions = [
    "//button[@type='button' and contains(text(), 'Continue')]",
    "//img[@alt='hammer']",
    "//a[@href='/daily']",
    "//button[not(contains(@class, 'pointer-events-none')) and contains(., 'Day')]",
]


with open("proxy.txt", "r", encoding="utf-8") as file:
    for line in file:
        proxy.append(line.strip())


def run_profile(i):
    user_data_dir = getUserDataDir(i)
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
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
            
        try:
            # Nhập password ví
            try:
                timesSleep()
                input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='swal2-input']"))
                )
                input_field.send_keys(230602)

                timesSleep(5)
                buttonUnlock = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Unlock')]"))
                )
                buttonUnlock.click()
            except Exception as e:
                print("Không cần nhập ví")
            # Kêt thúc nhập password ví
                
            timesSleep(3)
            buttonApprove = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Approve')]"))
            )
            buttonApprove.click()

        except Exception as e:
            print("Đã điểm danh rồi")
    except Exception as e:
        print(f"Không thể click vào tab 'Earn': {e}")

    time.sleep(5)
    driver.quit()


with concurrent.futures.ThreadPoolExecutor(max_workers=numberThreads) as executor:
    executor.map(run_profile, range(1, countProject + 1))
