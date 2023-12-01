import requests
import os
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

load_dotenv()

def line_notify_image(message,filename):
    line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    files = {'imageFile': open(filename, 'rb')}
    requests.post(line_notify_api, data=payload, headers=headers, files=files)

def main():
    filename = "screenshot.png"

    # クローラーの起動
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.binary_location = '/usr/bin/chromium-browser'
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Firefox()

    # 指定したドライバの要素が見つかるまでの待ち時間を2秒に設定
    driver.implicitly_wait(2)

    # APLのページを開く
    driver.get('https://apl.peerx-press.org/cgi-bin/main.plex')   
    time.sleep(2)

    # ログイン
    mail = driver.find_element(By.ID, 'login')
    password = driver.find_element(By.ID, 'password')

    mail.clear()
    password.clear()

    mail.send_keys(os.getenv('MAIL'))
    password.send_keys(os.getenv('PASSWORD'))
    mail.submit()

    time.sleep(2)

    # Live Manuscriptsをクリック
    driver.find_element(By.ID, 'DisplayTasks-add_ndt_task-9111-3').click()
    time.sleep(2)

    # 論文リンクをクリック
    driver.find_element(By.ID, 'DisplayTasks-add_ndt_task_table_row-9204-1').click()
    time.sleep(2)

    # Check Statusをクリック
    driver.find_element(By.LINK_TEXT, 'Check Status').click()
    time.sleep(2)

    # Statusをスクリーンショット
    png = driver.find_element(By.CLASS_NAME, 'dump_history_table').screenshot_as_png
    time.sleep(2)

    # ファイルに保存
    with open(filename, 'wb') as picture:
        picture.write(png)

    # Statusに変更があるかチェック
    status = driver.find_element(By.CLASS_NAME, 'dump_history_table').text
    print(status)
    flag = True
    with open('./status.txt', 'r') as log:
        prev = log.read()
        flag = (prev != status)

    # 変更があった場合、ステータスを更新しLINEに通知
    if flag:
        with open('./status.txt', 'w') as log:
            log.write(status)
        line_notify_image("Status has changed!", filename)
        print("\nStatus has changed!")
    else:
        print("\nStatus has not changed.")

    
    # クローラーの終了
    driver.quit()
    
main()