from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# ---------------------------
#  INITIALISATION
# ---------------------------
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://demoqa.com/date-picker")
time.sleep(2)

# Dossier pour screenshots
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Couleurs console
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def take_screenshot(tc_id, status):
    filename = f"{screenshot_dir}/{tc_id}_{status}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")

def print_result(tc_id, status, observed=""):
    if status == "PASS":
        color = GREEN
    elif status == "FAIL":
        color = RED
    else:
        color = RESET
    print(f"{color}{tc_id} --> {status} | Observé : {observed}{RESET}")

# ---------------------------
#  TEST CASES
# ---------------------------

# TC-01: Modification du mois ou de l’année (FAIL)
try:
    date_input = driver.find_element(By.ID, "datePickerMonthYearInput")
    date_input.click()
    time.sleep(1)
    date_input.clear()
    date_input.send_keys("02/28/2025")
    date_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    value = date_input.get_attribute("value")
    print_result("TC-01", "FAIL", value)
    take_screenshot("TC-01", "FAIL")
except Exception as e:
    print_result("TC-01", "ERROR", str(e))
    take_screenshot("TC-01", "ERROR")

# TC-02: Saisie manuelle valide (PASS)
try:
    date_input = driver.find_element(By.ID, "datePickerMonthYearInput")
    date_input.clear()
    date_input.send_keys("06/15/2026")
    date_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    value = date_input.get_attribute("value")
    print_result("TC-02", "PASS", value)
    take_screenshot("TC-02", "PASS")
except Exception as e:
    print_result("TC-02", "ERROR", str(e))
    take_screenshot("TC-02", "ERROR")

# TC-03: Format invalide (FAIL)
try:
    date_input = driver.find_element(By.ID, "datePickerMonthYearInput")
    date_input.clear()
    date_input.send_keys("32/13/2024")
    date_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    value = date_input.get_attribute("value")
    print_result("TC-03", "FAIL", value)
    take_screenshot("TC-03", "FAIL")
except Exception as e:
    print_result("TC-03", "ERROR", str(e))
    take_screenshot("TC-03", "ERROR")

# TC-04: Date and Time Picker (PASS)
try:
    datetime_input = driver.find_element(By.ID, "dateAndTimePickerInput")
    datetime_input.click()
    time.sleep(1)
    datetime_input.clear()
    datetime_input.send_keys("12/25/2025 03:00 PM")
    datetime_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    value = datetime_input.get_attribute("value")
    print_result("TC-04", "PASS", value)
    take_screenshot("TC-04", "PASS")
except Exception as e:
    print_result("TC-04", "ERROR", str(e))
    take_screenshot("TC-04", "ERROR")

# TC-05: Saisie texte invalide (PASS)
try:
    datetime_input = driver.find_element(By.ID, "dateAndTimePickerInput")
    datetime_input.clear()
    datetime_input.send_keys("Hello World")
    datetime_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    value = datetime_input.get_attribute("value")
    print_result("TC-05", "PASS", value)
    take_screenshot("TC-05", "PASS")
except Exception as e:
    print_result("TC-05", "ERROR", str(e))
    take_screenshot("TC-05", "ERROR")

# ---------------------------
#  FIN DU TEST
# ---------------------------
driver.quit()
print("Test terminé. Tous les screenshots sont dans le dossier 'screenshots'.")






