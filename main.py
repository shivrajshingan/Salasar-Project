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
URL = "http://local.salasarauction.com/admin/"
USERNAME = ""  # <- Fill your admin username
PASSWORD = ""  # <- Fill your admin password
BACKDATED_AUCTION_ID = "7190"
TODAY = "2025-07-16"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

def print_status(step, result):
    print(f"{step}: {'✅ PASS' if result else '❌ FAIL'}")

try:
    # Login
    driver.get(URL)
    driver.maximize_window()
    wait.until(EC.presence_of_element_located((By.NAME, "uname"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "pass").send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.NAME, "B1"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "forward")))

    # Forward > All
    wait.until(EC.element_to_be_clickable((By.ID, "forward"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "all"))).click()

    # Add Auction
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "addauction")))
    driver.execute_script("arguments[0].click();", add_button)

    # Switch to iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframes[0])

    # Get Auction ID (Store directly instead of copying)
    saleno_input = wait.until(EC.presence_of_element_located((By.ID, "saleno")))
    auction_id = saleno_input.get_attribute("value")
    print(f"📋 Auction ID = {auction_id}")

    # Copy Backdated Auction
    wait.until(EC.element_to_be_clickable((By.ID, "select2-chosen-2"))).click()
    search_input = wait.until(EC.presence_of_element_located((By.ID, "s2id_autogen2_search")))
    search_input.send_keys(BACKDATED_AUCTION_ID)
    search_input.send_keys(Keys.ENTER)

    # Fill Auction Form
    driver.find_element(By.ID, "auc_start_date").send_keys(TODAY)
    try:
        driver.find_element(By.ID, "auction_date").send_keys(TODAY)
    except NoSuchElementException:
        print("⚠️ auction_date not found, skipping")

    driver.find_element(By.NAME, "bshh").send_keys("12")
    driver.find_element(By.NAME, "bsmm").send_keys("00")
    driver.find_element(By.NAME, "bsss").send_keys("00")
    driver.find_element(By.NAME, "behh").send_keys("12")
    driver.find_element(By.NAME, "bemm").send_keys("30")
    driver.find_element(By.NAME, "bess").send_keys("00")
    driver.find_element(By.ID, "autocomplete").send_keys("Thane")

    driver.execute_script("window.scrollBy(0, 700);")
    wait.until(EC.element_to_be_clickable((By.ID, "submit_btn"))).click()
    print_status("Auction Form Submit", True)

    # Exit iframe
    driver.switch_to.default_content()

    # Search Auction by ID
    saleno_field = wait.until(EC.presence_of_element_located((By.NAME, "saleno")))
    saleno_field.clear()
    saleno_field.send_keys(auction_id)
    wait.until(EC.element_to_be_clickable((By.NAME, "R1"))).click()

    # Click Lots
    wait.until(EC.element_to_be_clickable((By.ID, "lots"))).click()

    # Select auction in lots page
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-container"))).click()
    lot_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-input")))
    lot_input.send_keys(BACKDATED_AUCTION_ID)
    lot_input.send_keys(Keys.ENTER)

    # Fetch lots
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID, "fetchLotsBtn"))).click()
    print_status("Lots Fetched", True)

    # Back to All auction page
    wait.until(EC.element_to_be_clickable((By.ID, "all"))).click()
    saleno_field = wait.until(EC.presence_of_element_located((By.NAME, "saleno")))
    saleno_field.clear()
    saleno_field.send_keys(auction_id)
    wait.until(EC.element_to_be_clickable((By.NAME, "R1"))).click()

    # Publish Auction
    pub_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pub_btn")))
    driver.execute_script("arguments[0].click();", pub_btn)
    print_status("Auction Published", True)

except Exception as e:
    print("❌ Exception:", e)
    driver.save_screenshot("error_screenshot.png")
    print("📸 Screenshot saved: error_screenshot.png")

finally:
    time.sleep(5)
    driver.quit()
