from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# ---------------------------
#  CONFIGURATION SELENIUM
# ---------------------------

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://demoqa.com/alerts")

wait = WebDriverWait(driver, 10)


# ---------------------------
#  FONCTION CAPTURE D’ÉCRAN
# ---------------------------

def take_screenshot(name):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    driver.save_screenshot(f"screenshots/{name}.png")
    print(f" Capture enregistrée : screenshots/{name}.png")


# ---------------------------
#  TC-01 : Simple Alert
# ---------------------------

def test_simple_alert():
    print("\n=== TC-01 Simple Alert ===")

    driver.find_element(By.ID, "alertButton").click()

    alert = wait.until(EC.alert_is_present())
    print("Alerte détectée :", alert.text)

    alert.accept()
    take_screenshot("TC01_simple_alert")

    print("→ Test Simple Alert : PASS")


# ---------------------------
#  TC-02 : Timed Alert
# ---------------------------

def test_timed_alert():
    print("\n=== TC-02 Timed Alert ===")

    driver.find_element(By.ID, "timerAlertButton").click()

    alert = wait.until(EC.alert_is_present())
    print("Alerte détectée après délai :", alert.text)

    alert.accept()
    take_screenshot("TC02_timed_alert")

    print("→ Test Timed Alert : PASS")


# ---------------------------
#  TC-03 : Confirm Alert
# ---------------------------

def test_confirm_alert():
    print("\n=== TC-03 Confirm Alert ===")

    driver.find_element(By.ID, "confirmButton").click()

    alert = wait.until(EC.alert_is_present())
    print("Texte de l’alerte :", alert.text)

    alert.accept()  # important : fermer avant interaction

    message = driver.find_element(By.ID, "confirmResult").text
    print("Message affiché :", message)

    assert "Ok" in message

    take_screenshot("TC03_confirm_alert")

    print("→ Test Confirm Alert : PASS")




try:
    test_simple_alert()
    test_timed_alert()
    test_confirm_alert()

    driver.save_screenshot("screenshots/redirect_success.png")
    print(" Screenshot final sauvegardé : redirect_success.png")

except Exception as e:
    print(" Test échoué :", e)

    # si une alerte est ouverte → la fermer pour permettre la capture
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    driver.save_screenshot("screenshots/redirect_error.png")
    print(" Screenshot erreur sauvegardé : redirect_error.png")

finally:
    print("\nTous les tests ont été exécutés.")
    driver.quit()
