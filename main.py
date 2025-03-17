from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import pandas as pd
import time
import json
from data import condition
from options import chrome_options

capabilities = chrome_options.to_capabilities()
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

driver = webdriver.Chrome(options=chrome_options)

# 啟用監聽器
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

job_detail_arr = []
condition_arr = []
found = False

# 監聽 Network.responseReceived 事件
def intercept_responses() :
    global found
    found = False
    time.sleep(1)
    logs = driver.get_log("performance")  # 獲取 Performance log
    for entry in logs :
        message = json.loads(entry["message"])["message"]
        if message["method"] == "Network.responseReceived" :
            if log_response(message.get("params", {})) :
                break
    if not found :
        job_detail_arr.append("API not found")
        condition_arr.append("API not found")

def log_response(response) :
    global found
    if "response" not in response :
        return False
    url = response["response"].get("url", "")
    if "/job/ajax/content" in url :
        found = True
        request_id = response["requestId"]  # 獲取請求識別碼
        time.sleep(0.5)
        try :
            response_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            decoded_data = json.loads(response_body["body"])
            job_detail_arr.append(decoded_data["data"]["jobDetail"]["jobDescription"])
            condition_arr.append(condition(decoded_data["data"]["condition"]))
            return True
        except :
            job_detail_arr.append("Unstable network connection...")
            condition_arr.append("Unstable network connection...")
            print(f"something is error: {url}")
            return True


def main( keyword: str, city: str, position: str, pages: int) :
    driver.get("https://www.104.com.tw/jobs/main/")
    driver.implicitly_wait(5)
    driver.maximize_window()
    # driver.save_screenshot("/app/screenshots/debug.png")

    # 選擇市區
    if city :
        try :
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/div[1]/div/div/form/div/div/div[1]/div/div[1]/button").click()
        except :
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[2]/div[1]/div/div/form/div/div/div[1]/div/div[1]/button").click()
        driver.find_element(By.CLASS_NAME,"category-picker-o-search").click()
        driver.find_element(By.CLASS_NAME,"search-bar").send_keys(city)
        try :
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div/ul/li[1]/label/span[1]/input").click()
        except : 
            driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div/div[2]/div/ul/li[1]/label/span[1]/input").click()
        driver.find_element(By.CLASS_NAME,"category-picker-btn-primary").click()
    
    # 選擇職務類別
    if position :
        try :
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/div[1]/div/div/form/div/div/div[1]/div/div[2]/button").click()
        except :
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[2]/div[1]/div/div/form/div/div/div[1]/div/div[2]/button").click()
        driver.find_element(By.CLASS_NAME,"category-picker-o-search").click()
        driver.find_element(By.CLASS_NAME,"search-bar").send_keys(position)
        try :
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div/ul/li[1]/label/span[1]/input").click()
        except :
            driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div/div[2]/div/ul/li[1]/label/span[1]/input").click()
        driver.find_element(By.CLASS_NAME,"category-picker-btn-primary").click()

    textInput = driver.find_element("css selector", f"input[placeholder='關鍵字(例：工作職稱、公司名、技能專長...)']")
    textInput.clear()
    textInput.send_keys(keyword)
    textInput.send_keys(Keys.RETURN)

    n = 0
    while n < pages :
        time.sleep(2.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        n+=1

    last_update_date = driver.find_elements(By.CLASS_NAME, "date-container")
    titleTages = driver.find_elements(By.CLASS_NAME,"info-job__text")
    company = driver.find_elements(By.CLASS_NAME,"info-company__text")
    location = driver.find_elements(By.XPATH,"//div[@class='info-tags gray-deep-dark']/span[1]")
    experience = driver.find_elements(By.XPATH,"//div[@class='info-tags gray-deep-dark']/span[2]")
    # education = driver.find_elements(By.XPATH,"//div[@class='info-tags gray-deep-dark']/span[3]")
    pay = driver.find_elements(By.XPATH,"//div[@class='info-tags gray-deep-dark']/span[4]/a")
    # detail = driver.find_elements(By.XPATH,"//div[@class='info-container']/div[4]")

    arr, url_arr = [], []
    now = time.localtime()
    file_name = f"{now.tm_year}-{now.tm_mon}-{now.tm_mday}_{keyword if keyword != '' else position}_{city}"
    file_name = file_name.replace("#", "Sharp")
    n = 0
    while len(titleTages) > n :
        job = []
        try :
            job.append(last_update_date[n].text)
            job.append(titleTages[n].text)
            job.append(company[n].text)
            job.append(location[n].text)
            job.append(experience[n].text)
            job.append(pay[n].text)
            job.append(titleTages[n].get_attribute("href"))
            url_arr.append(titleTages[n].get_attribute("href"))
            job.append(fr'=HYPERLINK("{file_name}/info_{n}.txt", "點擊查看")')
            job.append(fr'=HYPERLINK("{file_name}/condition_{n}.txt", "點擊查看")')
        except :
            print(f"index is over range: {n}")
            break
        arr.append(job)
        n+=1

    # save file
    relative_folder = Path(f"104/{file_name}")
    relative_folder.mkdir(parents=True, exist_ok=True)
    file_path = Path("104") / f"{file_name}.xlsx"
    df = pd.DataFrame(arr, columns=["最後更新日期", "職稱", "公司", "區域", "經歷", "待遇", "URL", "工作內容", "條件要求"])
    df.to_excel(file_path, index=False)

    for url in url_arr :
        driver.get(url)
        intercept_responses()
    
    for i in range(len(job_detail_arr)) :
        with open(f"104/{file_name}/info_{i}.txt", "w", encoding="utf-8") as f :
            f.write(job_detail_arr[i])
        with open(f"104/{file_name}/condition_{i}.txt", "w", encoding="utf-8") as f :
            f.write(condition_arr[i])
            
    driver.quit()

if __name__ == "__main__" :
    # 參數依序為 - 關鍵字, 市區, 職務類別, 資料篇幅(一頁約20筆)
    main("軟體工程師", "高雄市", "軟體工程師", 3)