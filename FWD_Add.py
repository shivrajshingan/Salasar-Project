from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Config
URL = "https://admin2.salasarauction.com/admin/"
ADMIN_USERNAME = "Demo"
ADMIN_PASSWORD = "Demo"
BACKDATED_AUCTION_ID = "7713"
TODAY = "2025-07-23"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def print_status(step, result):
    print(f"{step}: {'PASS' if result else 'FAIL'}")

try:
    driver.get(URL)
    driver.maximize_window()

    wait.until(EC.presence_of_element_located((By.NAME, "uname"))).send_keys(ADMIN_USERNAME)
    driver.find_element(By.NAME, "pass").send_keys(ADMIN_PASSWORD)

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
        driver.quit()
        exit()

    # Forward & All buttons
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

    # Click Add Auction
    try:
        add_button = wait.until(EC.element_to_be_clickable((By.ID, "addauction")))
        try:
            add_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", add_button)
        print_status("Add Button Click", True)

        # Switch to iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframe(s).")
        for idx, frame in enumerate(iframes):
            print(f"Iframe {idx}: id={frame.get_attribute('id')}, name={frame.get_attribute('name')}")
        if iframes:
            driver.switch_to.frame(iframes[0])
            print("Switched to first iframe.")

    except Exception as e:
        print_status("Add Button Click", False)
        print(str(e))

    # Copy Auction ID
    input1 = driver.find_element(By.ID, "saleno")
    actions.click(input1).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

    # Copy Backdated Auction
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "select2-chosen-2"))).click()
        print_status("Copy Backdated Auction Button Click", True)
    except Exception as e:
        print_status("Copy Backdated Auction Button Click", False)
        print(str(e))

    try:
        search_input = wait.until(EC.presence_of_element_located((By.ID, "s2id_autogen2_search")))
        search_input.send_keys(BACKDATED_AUCTION_ID)
        search_input.send_keys(Keys.ENTER)
        print_status("Entered and Selected Auction Number", True)
    except Exception as e:
        print_status("Failed to Enter Auction Number", False)
        print(str(e))

    # Fill Auction Form
    try:
        driver.find_element(By.ID, "startdate").send_keys(TODAY)
        try:
            driver.find_element(By.ID, "auction_date").send_keys(TODAY)
        except NoSuchElementException:
            print("'auction_date' not found. Skipping.")

        driver.find_element(By.NAME, "bshh").send_keys("09")
        driver.find_element(By.NAME, "bsmm").send_keys("30")
        driver.find_element(By.NAME, "bsss").send_keys("00")
        driver.find_element(By.NAME, "behh").send_keys("20")
        driver.find_element(By.NAME, "bemm").send_keys("00")
        driver.find_element(By.NAME, "bess").send_keys("00")
        # location_input = wait.until(EC.presence_of_element_located((By.ID, "autocomplete")))
        # location_input.clear()
        # location_input.send_keys("Thane, Maharashtra, India")
        # time.sleep(5)
        # # Wait and click on the first dropdown suggestion
        # first_suggestion = wait.until(EC.element_to_be_clickable(
        # (By.XPATH, "//span[text()='Thane, Maharashtra, India']")))
        # first_suggestion.click()
        driver.find_element(By.ID, "catalogue_id").send_keys("0")
        time.sleep(5)

        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(5)
        wait.until(EC.element_to_be_clickable((By.ID, "submit_btn"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "submit_btn"))).click()
        print_status("Auction Added", True)
    except Exception as e:
        print_status("Auction Filled", False)
        print(str(e))
        
    # Paste Auction ID in All Auction list
    driver.switch_to.default_content()
    wait.until(EC.presence_of_element_located((By.NAME, "saleno"))).click()
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    wait.until(EC.element_to_be_clickable((By.NAME, "R1"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "lots"))).click()

    # Select Auction Lots
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-container"))).click()
        search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-input")))
        search_input.send_keys(BACKDATED_AUCTION_ID)
        search_input.send_keys(Keys.ENTER)
        print_status("Entered and Selected Auction Lots", True)
    except Exception as e:
        print_status("Failed to Enter Auction Lots", False)
        print("Exception:", str(e))

        # Fetch Lots Button
    try:
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "fetchLotsBtn"))).click()
        time.sleep(2)
        search_input.send_keys(Keys.ENTER)
        print_status("Fetch lots", True)
    except Exception as e:
        print_status("Fetch lots", False)
        print("Exception:", str(e))

        # All Auction
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "all"))).click()
        print_status("All Click", True)
    except Exception as e:
        print_status("All Click", False)
        print(str(e))

        # Paste Auction ID in SaleNo list
    try:
        saleno_input = wait.until(EC.presence_of_element_located((By.NAME, "saleno")))
        saleno_input.click()
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        print_status("saleno field", True)
    except Exception as e:
        print_status("not filled sale no", False)
        print("Exception:", str(e))

        time.sleep(2)

    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "R1"))).click()

    #Auction Publish
        img_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pub_btn")))
        img_button.click()
        print_status("Clicked Publish Icon", True)
    except Exception as e:
        print_status("Clicked Publish Icon", False)
        print("Exception:", str(e))

finally:
    time.sleep(10)
    driver.quit()
