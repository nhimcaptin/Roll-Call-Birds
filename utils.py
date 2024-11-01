import time
from selenium.webdriver.common.by import By
import urllib.parse
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

chrome_driver_path = r"E:\Airdrop\Resources\chromedriver-win64\chromedriver.exe"


def timesSleep(max=2):
    random_number = random.uniform(0.5, max)
    time.sleep(random_number)


def getUserDataDir(index):
    return rf"C:\Users\doanh.tran\AppData\Local\Google\Chrome\User Data\Profile {index}"


def getInformationWorm(driver, buttonInformation):
    try:
        informationWorm = []
        for information in buttonInformation:
            timesSleep()
            value = driver.find_element(By.XPATH, information[0]).text
            count = driver.find_element(By.XPATH, information[1]).text.split("x")[1]
            print("count", value, count)
            informationWorm.append(
                {"value": int(value), "count": int(count), "XPath": information[2]}
            )
        return informationWorm
    except Exception as e:
        print(f"Lỗi: {e}")


def allActionWorm(count, data):
    results = []
    while count > 0:
        if (
            count >= data[2]["value"]
            and results.count(data[2]["value"]) < data[2]["count"]
        ):
            count -= data[2]["value"]
            results.append(data[2]["XPath"])
        elif (
            count >= data[1]["value"]
            and results.count(data[1]["value"]) < data[1]["count"]
        ):
            count -= data[1]["value"]
            results.append(data[1]["XPath"])
        elif (
            count >= data[0]["value"]
            and results.count(data[0]["value"]) < data[0]["count"]
        ):
            count -= data[0]["value"]
            results.append(data[0]["XPath"])

    return results


def authenticationWallet(driver):
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
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Unlock')]")
                )
            )
            buttonUnlock.click()
        except Exception as e:
            print("Không cần nhập ví")
        # Kêt thúc nhập password ví

        timesSleep(3)
        buttonApprove = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Approve')]")
            )
        )
        buttonApprove.click()

    except Exception as e:
        print("Đã xác thực giao dịch thành công")


def clickButton(driver, XPATH, message=""):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPATH))
        )
        timesSleep(5)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, XPATH))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            button,
        )
        timesSleep(1)
        button.click()
        return False
    except Exception as e:
        if message:
           print(message)
           return True
        else: 
            pass


def action_play_game(driver):
    try:
        try:
            button_play = driver.find_element(
                By.XPATH,
                '//div[@class="new-message-bot-commands is-view"]//div[@class="new-message-bot-commands-view"]',
            )
            button_play.click()
            print("Đã nhấn nút 'Play'")
            time.sleep(5)
        except Exception as e:
            pass

        try:
            button_open_app = driver.find_elements(
                By.XPATH,
                '//button[.//span[text()="Open App" or text()="Mở chương trình"]]',
            )
            button_open_app[len(button_open_app) - 1].click()
            print("Đã nhấn nút 'Open App'")
            time.sleep(1)
        except Exception as e:
            pass

        try:
            button_confirm = driver.find_element(
                By.XPATH, '//button[span[text()="Confirm"]]'
            )
            if button_confirm:
                button_confirm.click()
                print("Đã nhấn nút 'Confirm'")
                time.sleep(1)
        except Exception as e:
            pass

        try:
            launch_button = driver.find_element(
                By.XPATH, "//button[span[text()='Launch']]"
            )
            if launch_button:
                launch_button.click()
                print("Đã nhấn nút 'Launch'")
                time.sleep(1)
        except Exception as e:
            pass

    except Exception as e:
        print(f"Không thể start game: ", e)


def sort_data_by_user_id():
    with open("file_user_ids.txt", "r", encoding="utf-8") as f:
        user_ids = f.read().splitlines()

    with open("data.txt", "r", encoding="utf-8") as f:
        query_data = f.read().splitlines()

    decoded_queries = [urllib.parse.unquote(query) for query in query_data]

    query_dict = {}
    for index, query in enumerate(decoded_queries):
        user_id_match = re.search(r'"id":(\d+)', query)
        if user_id_match:
            user_id = int(user_id_match.group(1))
            query_dict[user_id] = query_data[index]

    sorted_queries = [
        query_dict[int(user_id)] for user_id in user_ids if int(user_id) in query_dict
    ]

    sorted_data_queries = "\n".join(sorted_queries)

    with open("data.txt", "w", encoding="utf-8") as f:
        f.write(sorted_data_queries)
