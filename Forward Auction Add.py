from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import pyperclip

# Config
URL = "http://local.salasarauction.com/admin/"
USERNAME = "Demo"
PASSWORD = "Demo"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

def print_status(step, result):
    print(f"{step}: {'PASS' if result else 'FAIL'}")

try:
    # Step 1: Open admin login page
    driver.get(URL)
    driver.maximize_window()

    # Step 2: Login
    wait.until(EC.presence_of_element_located((By.NAME, "uname"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "pass").send_keys(PASSWORD)
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "B1")))
        login_button.click()
    except:
        driver.execute_script("arguments[0].click();", driver.find_element(By.NAME, "B1"))

    time.sleep(2)

    # Step 3: Login success check
    try:
        wait.until(EC.presence_of_element_located((By.ID, "forward")))
        print_status("Login Check", True)
    except:
        print_status("Login Check", False)
        driver.quit()
        exit()

    # Step 4: Forward & All buttons
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "forward"))).click()
        print_status("Forward Button Click", True)
    except:
        print_status("Forward Button Click", False)

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "all"))).click()
        print_status("All Click", True)
    except:
        print_status("All Click", False)

    # Step 5: Click Add Auction
    try:
        add_button = wait.until(EC.element_to_be_clickable((By.ID, "addauction")))
        try:
            add_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", add_button)
        print_status("Add Button Click", True)

        time.sleep(3)
        # driver.save_screenshot("after_add_click.png")
        # print("Screenshot saved: after_add_click.png")

        # Detect and switch to iframe if exists
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframe(s).")
        for idx, frame in enumerate(iframes):
            print(f"Iframe {idx}: id={frame.get_attribute('id')}, name={frame.get_attribute('name')}")
        if len(iframes) > 0:
            driver.switch_to.frame(iframes[0])
            print("Switched to first iframe.")

    except (TimeoutException, NoSuchElementException) as e:
        print_status("Add Button Click", False)
        raise e
    
    # Copy Auction ID
    
    input1 = driver.find_element(By.ID, "saleno")
    input1.send_keys(Keys.CONTROL, 'a')   # Select All
    input1.send_keys(Keys.CONTROL, 'c')   # Copy
    time.sleep(1)
    
        # Copy Backdated Auction   
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "select2-chosen-2"))).click()
        print_status("Copy Backdated Auction Button Click", True)
    except:
        print_status("Copy Backdated Auction Button Click", False)

    try:
        # Focus on the input
        search_input = wait.until(EC.presence_of_element_located((By.ID, "s2id_autogen2_search")))
        search_input.click()
        search_input.send_keys("7215")
        search_input.send_keys(Keys.ENTER)
        print_status("Entered and Selected Auction Number", True)
    except:
        print_status("Failed to Enter Auction Number", False)

        time.sleep(5)

    # Step 6: Fill Form
    try:
        # wait.until(EC.presence_of_element_located((By.ID, "auctype"))).send_keys("Forward Auction")
        driver.find_element(By.ID, "auc_start_date").send_keys("2025-06-19")  # Start Date

        # Try to locate end date field with fallback
        try:
            driver.find_element(By.ID, "auction_date").send_keys("2025-06-20")
        except NoSuchElementException:
            print("End date field with ID 'id4' not found. Skipping.")
            # driver.save_screenshot("missing_end_date_field.png")

        driver.find_element(By.NAME, "bshh").send_keys("11")
        driver.find_element(By.NAME, "bsmm").send_keys("00")
        driver.find_element(By.NAME, "bsss").send_keys("00")
        Select(driver.find_element(By.ID, "auccomp")).select_by_visible_text("Jindal Polyfilms Ltd (Unit: Nasik, Maharashtra) (AA0520A01)")

        # Updated location autocomplete logic
        # try:
        #     location_input = wait.until(EC.element_to_be_clickable((By.NAME, "autocomplete")))
        #     driver.execute_script("arguments[0].scrollIntoView(true);", location_input)
        #     time.sleep(0.5)
        #     location_input.clear()
        #     location_input.send_keys("Thane")
        #     print_status("Location Field Entry", True)
        # except Exception as e:
        #     print_status("Location Field Entry", False)
        #     driver.save_screenshot("location_field_issue.png")
        #     print("Location input not interactable. Screenshot saved.")

        driver.find_element(By.NAME, "behh").send_keys("18")
        driver.find_element(By.NAME, "bemm").send_keys("50")
        driver.find_element(By.NAME, "bess").send_keys("00")
        driver.find_element(By.ID, "aucpartcular").send_keys("auctomationtest")
        driver.find_element(By.ID, "autocomplete").send_keys("Thane")
        driver.execute_script("window.scrollBy(0, 500);")
        # driver.find_element(By.ID, "location").send_keys("Thane")
        # Select(driver.find_element(By.ID, "auc_owner")).select_by_visible_text("Disha Dhara")
        # Select(driver.find_element(By.ID, "auc_rm")).select_by_visible_text("Disha Dhara")
        # Select(driver.find_element(By.ID, "auc_handler")).select_by_visible_text("Disha Dhara")
        # driver.find_element(By.ID, "catalogue_id").send_keys("1234")
        # Select(driver.find_element(By.ID, "bid_logic")).select_by_visible_text("Default")
        time.sleep(15)
        driver.find_element(By.ID, "submit_btn").click()

        print_status("Auction Added", True)

    except TimeoutException:
        print_status("Auction Filled", False)

        # All Auction list
        time.sleep(6)
        input2 = driver.find_element(By.NAME, "saleno")
        input2.click()
        input2.send_keys(Keys.CONTROL, 'v')       

finally:
    time.sleep(15)
    driver.quit()