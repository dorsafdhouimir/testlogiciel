from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style
import time
import os
# --------------------------------------------------------
#  FUNCTION : Log with colored status + emoji
# --------------------------------------------------------
def log_test(test_id, status):
    color = Fore.GREEN if status == "PASS" else Fore.RED
    icon = "✔️" if status == "PASS" else "❌"
    print(color + f"{test_id} : {status} {icon}" + Style.RESET_ALL)


# --------------------------------------------------------
#  MAIN TEST FUNCTION
# --------------------------------------------------------
def test_books():

    # Start timer
    start_time = time.time()

    # Create screenshots folder
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    driver.get("https://demoqa.com/books")

    results = {}

    # --------------------------------------------------------
    # TC-BS-01 : Liste des livres
    # --------------------------------------------------------
    try:
        books = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rt-tr-group")))
        valid_books = [
            b for b in books
            if b.find_element(By.CSS_SELECTOR, ".rt-td:nth-child(2)").text.strip()
        ]
        results["TC-BS-01"] = "PASS" if valid_books else "FAIL"

    except Exception:
        driver.save_screenshot("screenshots/TC-BS-01.png")
        results["TC-BS-01"] = "FAIL"


    # --------------------------------------------------------
    # TC-BS-02 : Recherche
    # --------------------------------------------------------
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchBox")))
        search_box.clear()
        search_box.send_keys("Git")

        filtered_books = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rt-tr-group")))
        titles = [
            b.find_element(By.CSS_SELECTOR, ".rt-td:nth-child(2)").text.strip()
            for b in filtered_books
            if b.find_element(By.CSS_SELECTOR, ".rt-td:nth-child(2)").text.strip()
        ]

        results["TC-BS-02"] = "PASS" if titles and all("Git" in t for t in titles) else "FAIL"

    except:
        driver.save_screenshot("screenshots/TC-BS-02.png")
        results["TC-BS-02"] = "FAIL"


    # --------------------------------------------------------
    # TC-BS-03 : Pagination
    # --------------------------------------------------------
    try:
        driver.get("https://demoqa.com/books")
        next_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='next page']")

        if next_btn.is_enabled():
            next_btn.click()
            page2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rt-tr-group")))
            titles = [b.find_element(By.CSS_SELECTOR, ".rt-td:nth-child(2)").text.strip() for b in page2]
            results["TC-BS-03"] = "PASS" if titles else "FAIL"
        else:
            results["TC-BS-03"] = "FAIL"

    except:
        driver.save_screenshot("screenshots/TC-BS-03.png")
        results["TC-BS-03"] = "FAIL"


    # --------------------------------------------------------
    # TC-BS-04 : Détails d’un livre
    # --------------------------------------------------------
    try:
        driver.get("https://demoqa.com/books")
        link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rt-tr-group .rt-td:nth-child(2) a")))
        link.click()

        isbn = driver.find_elements(By.ID, "ISBN-wrapper")
        author = driver.find_elements(By.ID, "author-wrapper")
        publisher = driver.find_elements(By.ID, "publisher-wrapper")

        results["TC-BS-04"] = "PASS" if (isbn or author or publisher) else "FAIL"

    except:
        driver.save_screenshot("screenshots/TC-BS-04.png")
        results["TC-BS-04"] = "FAIL"


    # --------------------------------------------------------
    # TC-BS-05 : Tri par titre
    # --------------------------------------------------------
    try:
        driver.get("https://demoqa.com/books")
        title_header = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='columnheader' and text()='Title']")
        ))
        title_header.click()

        sorted_books = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".rt-tr-group .rt-td:nth-child(2)")
        ))

        titles = [b.text.strip() for b in sorted_books if b.text.strip()]
        results["TC-BS-05"] = "PASS" if titles == sorted(titles, key=str.lower) else "FAIL"

    except:
        driver.save_screenshot("screenshots/TC-BS-05.png")
        results["TC-BS-05"] = "FAIL"


    # Close browser
    driver.quit()

    # End timer
    end_time = time.time()
    duration = round(end_time - start_time, 2)


    # --------------------------------------------------------
    # REPORTING
    # --------------------------------------------------------
    print("\n========== 📊 AUTOMATION REPORT ==========")
    for tc, status in results.items():
        log_test(tc, status)
    print("==========================================")
    print(f"⏳ Execution Time : {duration} seconds")

    # Export report
    with open("bookstore_report.txt", "w") as f:
        f.write("=== Book Store Automation Report ===\n")
        for tc, status in results.items():
            f.write(f"{tc} : {status}\n")
        f.write(f"\nExecution Time : {duration}s\n")

    print("📁 Report generated : bookstore_report.txt")
    print("📸 Screenshots saved in /screenshots folder")


# RUN SCRIPT
if __name__ == "__main__":
    test_books()
