from flask import Flask, render_template, redirect
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get("https://ermssec.assam.gov.in/panchayat/download-pdf-electoral-roll")
        # Wait for user to select data
        found = False
        for _ in range(180): # 3 minutes max wait
            rows = driver.find_elements(By.TAG_NAME, "tr")
            if len(rows) > 10:
                time.sleep(5)
                found = True
                break
            time.sleep(1)

        if found:
            rows = driver.find_elements(By.TAG_NAME, "tr")
            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 6:
                    data.append([c.text.strip() for c in cols])
            
            df = pd.DataFrame(data, columns=["Sl_No", "Name", "Relative", "Age", "Gender", "EPIC"])
            df.to_csv(f"Voter_{int(time.time())}.csv", index=False)
    finally:
        driver.quit()
        return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
