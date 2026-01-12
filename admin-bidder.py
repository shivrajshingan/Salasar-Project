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
ADMIN_URL = "https://admin2.salasarauction.com/admin/"
BIDDER_URL = "https://salasarauction.com/"
ADMIN_USERNAME = "demo"
ADMIN_PASSWORD = "demo"
BACKDATED_AUCTION_ID = "8580"
BIDDER_USERNAME = "demo"
BIDDER_PASSWORD = "demo"
TODAY = "2026-01-12"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def print_status(step, result):
    print(f"{step}: {'PASS' if result else 'FAIL'}")

try:
    # Open admin login page
    driver.get(ADMIN_URL)
    driver.maximize_window()

    # Login
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
        location_input = wait.until(EC.presence_of_element_located((By.ID, "autocomplete")))
        location_input.clear()
        location_input.send_keys("Thane, Maharashtra, India")
        time.sleep(5)
        # Wait and click on the first dropdown suggestion
        first_suggestion = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[text()='Thane, Maharashtra, India']")))
        first_suggestion.click()
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
    
    time.sleep(3)
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
        
    driver.get(BIDDER_URL)
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='80%'")

    # Bidder login
    wait.until(EC.element_to_be_clickable((By.ID, "bidder"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "uname1"))).send_keys(BIDDER_USERNAME)
    wait.until(EC.visibility_of_element_located((By.ID, "pass1"))).send_keys(BIDDER_PASSWORD)
    wait.until(EC.element_to_be_clickable((By.ID, "login"))).click()
    print("Login Successful")

    # Handle popup
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "notice"))).click()
        time.sleep(2)
        driver.execute_script("document.body.style.zoom='80%'")
        wait.until(EC.element_to_be_clickable((By.ID, "notice11"))).click()
        print("Popup closed.")
    except Exception as e:
        print("Popup not found or already closed:", e)

    # Forward Auction
    wait.until(EC.element_to_be_clickable((By.ID, "forward"))).click()
    print("Clicked on Forward Auction.")

    # Today's Auction
    wait.until(EC.element_to_be_clickable((By.ID, "Todays"))).click()
    print("Clicked on Today's Auction.")

    time.sleep(2)  # Allow list to load

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframe(s).")

    bidnow_clicked = False

    # Try inside each iframe
    for iframe in iframes:
        driver.switch_to.default_content()  # Always reset before switching
        driver.switch_to.frame(iframe)
        try:
            bid_button = wait.until(EC.presence_of_element_located((By.ID, "bidnow")))
            if bid_button.is_displayed() and bid_button.is_enabled():
                driver.execute_script("arguments[0].click();", bid_button)
                print("Clicked on Bid Now inside iframe.")
                bidnow_clicked = True
                break
        except Exception as e:
            print("'Bid Now' not found in this iframe:", e)
            continue

    driver.switch_to.default_content()  # Always return

    # If not clicked inside any iframe, try in main content
    if not bidnow_clicked:
        try:
            bid_button = wait.until(EC.element_to_be_clickable((By.ID, "bidnow")))
            driver.execute_script("arguments[0].click();", bid_button)
            print("Clicked on Bid Now in main content.")
        except Exception as e:
            print("Failed to click 'Bid Now' in main content:", e)

    # driver.execute_script("document.body.style.zoom='70%'")

    # Click Terms & Conditions
    try:
        invalid_elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "invalid")))
        invalid_elem.click()
        print("Clicked on Terms & Conditions.")
    except Exception as e:
        print("'invalid' class element not found or not clickable:", e)
        driver.save_screenshot("terms_invalid_error.png")
        print("Screenshot saved: terms_invalid_error.png")

    # Accept Terms
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "accept_term"))).click()
        print("Accept button clicked")
    except Exception as e:
        print("Accept button not clickable:", e)
        driver.save_screenshot("accept_term_error.png")

    # Bid button
    # driver.execute_script("document.body.style.zoom='70%'")
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "bid_1"))).click()
        print("Bid button clicked")
    except Exception as e:
        print("Bid button not clickable:", e)
        driver.save_screenshot("bid_button_error.png")

    # Submit bid
    time.sleep(3)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "btnSave"))).click()
        print("Bid Submitted")
    except Exception as e:
        print("Bid not Submitted:", e)

    time.sleep(3)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "close"))).click()
        print("close button click")
    except Exception as e:
        print("close button not Submitted:", e)
    time.sleep(3)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "bid_2"))).click()
        print("Bid button clicked")
    except Exception as e:
        print("Bid button not clickable:", e)
        driver.save_screenshot("bid_button_error.png")

    # Submit bid
    time.sleep(3)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "btnSave"))).click()
        print("Bid Submitted")
    except Exception as e:
        print("Bid not Submitted:", e)
    time.sleep(3)    

    driver.get(ADMIN_URL)
    driver.maximize_window()

    # Login
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
    print("Finished all steps.")
    time.sleep(10)
    driver.quit()

