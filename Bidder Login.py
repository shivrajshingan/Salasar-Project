from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuration
LOGIN_URL = "http://salasarauction.com/"
USERNAME = "Demo"
PASSWORD = "Demo"

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

try:
    driver.get(LOGIN_URL)
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='80%'")

    # Bidder login
    wait.until(EC.element_to_be_clickable((By.ID, "bidder"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "uname1"))).send_keys(USERNAME)
    wait.until(EC.visibility_of_element_located((By.ID, "pass1"))).send_keys(PASSWORD)
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
        print("📸 Screenshot saved: terms_invalid_error.png")

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
        print(" close button not Submitted:", e)    

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

finally:
    time.sleep(15)
    driver.quit()
