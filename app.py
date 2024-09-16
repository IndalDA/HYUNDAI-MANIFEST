from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

app = Flask(__name__)

# HTML template for running Selenium code
form_template = '''
<!doctype html>
<title>Run Selenium Code</title>
<h1>Run Selenium Code</h1>
<form action="/run_selenium" method="post">
  <input type="submit" value="Run Selenium Code" />
</form>
'''

@app.route('/')
def index():
    return render_template_string(form_template)

@app.route('/run_selenium', methods=['POST'])
def run_selenium_code():
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://hirise.honda2wheelersindia.com/siebel/app/edealer/enu/?SWECmd=Login&SWECM=S&SWEHo=hirise.honda2wheelersindia.com")
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_swepi_1"))).send_keys("DL010008PA001")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_swepi_2"))).send_keys("Hirise_5571")
    
    captcha_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "captchaCode")))
    captcha_text = captcha_label.text.replace(" ", "")
    captcha_input = driver.find_element(By.ID, "s_captcha")
    captcha_input.send_keys(captcha_text)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_swepi_22"))).click()
    time.sleep(4)
    driver.switch_to.alert.accept()
    time.sleep(4)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div/ul/li[5]/span"))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_smc_1800"))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_1_1_10_0_Ctrl"))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_1_1_7_0_Ctrl"))).click()
    time.sleep(2)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_at_m_1"))).click()
    time.sleep(2)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[6]/div/div[7]/div/div[1]/div/div[1]/div/form/span/div/div[1]/div[2]/span[1]/span/ul/li[23]/a'))).click()
    time.sleep(2)
    
    element_xpath = '/html/body/div[11]/div[2]/div/div/div/form/table/tbody/tr[2]/td/table/tbody/tr/td/span[2]/button'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_xpath))).click()
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    MAIN_FOLDER = "Honda 2W Auto"
    STKfolder_name = "STK"
    latest_file_name = "output.csv"
    new_file_name = "STK.csv"
    
    start_time = time.time()
    while not os.path.exists(os.path.join(download_folder, latest_file_name)):
        time.sleep(1)
    
    os.rename(
        os.path.join(download_folder, latest_file_name),
        os.path.join(download_folder, new_file_name)
    )
    
    destination_folder = os.path.join(desktop_path, MAIN_FOLDER, STKfolder_name)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    shutil.move(
        os.path.join(download_folder, new_file_name),
        os.path.join(destination_folder, new_file_name)
    )
    
    element_xpath = "/html/body/div[11]/div[2]/div/div/div/form/table/tbody/tr[1]/td/table/tbody/tr/td/table[1]/tbody/tr/td/span"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[2]/div/div/div/form/table/tbody/tr[2]/td/table/tbody/tr/td/span[3]')))
    element.click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div/ul/li[5]/span"))).click()

    driver.close()
    
    return "Selenium code executed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
