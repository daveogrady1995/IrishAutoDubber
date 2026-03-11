# selenium_utils.py (copied from source)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Use packaging helper to resolve bundled resource paths when frozen
# avoid top-level import that can create a circular import when frozen;
# resolve resource_path lazily inside `setup_selenium` instead


def setup_selenium(current_folder):
    chrome_options = Options()
    prefs = {
        "download.default_directory": current_folder,
        "download.prompt_for_download": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)

    # Resolve resource_path without importing dubbing_core to avoid
    # circular imports when frozen. Use sys._MEIPASS when available.
    def resource_path(p):
        import sys

        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base = sys._MEIPASS
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base, p)

    # When running as a PyInstaller bundle use the included chromedriver.
    # When running from source always use webdriver-manager so it
    # downloads a driver that matches the currently installed Chrome.
    import sys
    import platform

    if getattr(sys, "frozen", False):
        driver_filename = (
            "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
        )
        driver_path = resource_path(os.path.join("drivers", driver_filename))
        if os.path.exists(driver_path):
            service = Service(driver_path)
        else:
            service = Service(ChromeDriverManager().install())
    else:
        # Running from source – let webdriver-manager pick the right version
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://abair.ie/synthesis")

    wait = WebDriverWait(driver, 15)

    # Handle cookie banner
    try:
        cookie_accept_xpath = "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'got it') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ok')]"
        cookie_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, cookie_accept_xpath))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", cookie_btn
        )
        driver.execute_script("arguments[0].click();", cookie_btn)
        print("   > Cookie banner accepted.")
        time.sleep(2)
    except:
        print("   > No cookie banner detected or already accepted.")

    # Switch language to GA
    try:
        ga_xpath = "//button[.//span[contains(text(), 'GA')]]"
        lang_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ga_xpath)))
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", lang_btn
        )
        driver.execute_script("arguments[0].click();", lang_btn)
        print("   > Language switched to Irish (GA). Waiting for update...")
        time.sleep(2)
    except:
        print("   > NOTE: Could not switch language.")

    return driver, wait
