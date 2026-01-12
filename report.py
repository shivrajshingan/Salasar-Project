from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Config
URL = "https://admin2.salasarauction.com/admin/"
USERNAME = "salasar_admin"
PASSWORD = "Aonesalasar@AOSPL"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def print_status(step, result):
    print(f"{step}: {'✅ PASS' if result else ' FAIL'}")

try:
    # Open admin login page
    driver.get(URL)
    driver.maximize_window()

    # Login
    wait.until(EC.presence_of_element_located((By.NAME, "uname"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "pass").send_keys(PASSWORD)

    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "B1"))).click()
    except:
        driver.execute_script("arguments[0].click();", driver.find_element(By.NAME, "B1"))

    # Login success check
    try:
        wait.until(EC.presence_of_element_located((By.ID, "forward")))
        print_status("Login Check", True)
    except:
        print_status("Login Check", False)

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "forward"))).click()
        print_status("Forward Button Click", True)
    except Exception as e:
        print_status("Forward Button Click", False)
        print(str(e))

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "all"))).click()
        print_status("All Click", True)
    except Exception as e:
        print_status("All Click", False)
        print(str(e))

        wait.until(EC.presence_of_element_located((By.NAME, "saleno"))).click()
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    # Select radio button R1
    wait.until(EC.element_to_be_clickable((By.NAME, "R1"))).click()
    print_status("Radio R1 Click", True)

    # Lots button
    wait.until(EC.element_to_be_clickable((By.ID, "lots"))).click()
    print_status("Lots Click", True)

    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-container"))).click()
        search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-input")))
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        search_input.send_keys(Keys.ENTER)
        print_status("Entered and Selected Auction Lots", True)
    except Exception as e:
        print_status("Failed to Enter Auction Lots", False)
        print(" Exception:", str(e))

    try:
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "fetchresult"))).click()
        time.sleep(2)
        search_input.send_keys(Keys.ENTER)
        print_status("Fetch result", True)
    except Exception as e:
        print_status("Fetch result", False)
        print(" Exception:", str(e))
        driver.save_screenshot("auction_result.png")
        print("📸 Screenshot saved: auction_result.png")

finally:
    time.sleep(10)
    driver.quit()
