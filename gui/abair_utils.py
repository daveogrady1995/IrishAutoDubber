from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import glob
import os

# Import get_latest_file from helpers
from .helpers import get_latest_file


def set_abair_settings(driver, dialect, gender, wait):
    # --- SELECT DIALECT (Dropdown) ---
    try:
        select_xpath = "//div[./div/span[text()='Dialect']]/div/select"
        select_element = wait.until(
            EC.presence_of_element_located((By.XPATH, select_xpath))
        )
        dialect_select = Select(select_element)
        dialect_select.select_by_visible_text(dialect)
        time.sleep(1)  # Reduced from 3
        print(f"   > Dialect set to: {dialect}")
    except Exception as e:
        print(f"!!! FAIL: Error setting Dialect: {e}")
        return False

    # --- SELECT GENDER (Custom Button) ---
    try:
        gender_xpath = f"//div[./div/span[text()='Gender']]/div/button[contains(text(), '{gender}')]"
        gender_btn = wait.until(EC.element_to_be_clickable((By.XPATH, gender_xpath)))
        driver.execute_script("arguments[0].click();", gender_btn)
        time.sleep(1)  # Reduced from 3
        print(f"   > Gender set to: {gender}")
    except Exception as e:
        print(f"!!! FAIL: Error setting Gender: {e}")
        return False

    # --- SELECT VOICE FOR KERRY MALE (Danny) ---
    if dialect == "Kerry" and gender == "Male":
        try:
            voice_xpath = "//div[./div/span[text()='Voice']]/div/button[contains(text(), 'Danny')]"
            voice_btn = wait.until(EC.element_to_be_clickable((By.XPATH, voice_xpath)))
            driver.execute_script("arguments[0].click();", voice_btn)
            time.sleep(1)
            print(f"   > Voice set to: Danny")
        except Exception as e:
            print(f"!!! FAIL: Error setting Voice: {e}")
            return False

    # --- SELECT MODEL (AI) ---
    try:
        model_xpath = (
            f"//div[./div/span[text()='Model']]/div/button[contains(text(), 'AI')]"
        )
        model_btn = wait.until(EC.element_to_be_clickable((By.XPATH, model_xpath)))
        driver.execute_script("arguments[0].click();", model_btn)
        time.sleep(1)
        print(f"   > Model set to: AI")
    except Exception as e:
        print(f"!!! FAIL: Error setting Model: {e}")
        return False

    return True


def get_abair_audio(driver, text, download_folder, dialect, gender, wait):
    try:
        # Set settings
        if not set_abair_settings(driver, dialect, gender, wait):
            return None

        # Clean old files
        for old_file in glob.glob(os.path.join(download_folder, "synthesis*")):
            try:
                os.remove(old_file)
            except:
                pass

        text_area = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        text_area.clear()
        time.sleep(2)  # Increased delay
        text_area.send_keys(text)
        time.sleep(2)  # Increased delay after sending keys

        # Synthesize
        synth_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Synthesize')]")
            )
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", synth_btn
        )
        time.sleep(2)  # Increased delay
        synth_btn.click()
        time.sleep(5)  # Wait longer after synthesize click for processing

        # Wait for download button
        download_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Download')]"))
        )
        time.sleep(2)  # Increased delay
        before_click = time.time()
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", download_btn
        )
        download_btn.click()

        # Wait for file
        attempts = 0
        while attempts < 30:  # Increased max attempts
            time.sleep(1)
            latest = get_latest_file(download_folder)
            if (
                latest
                and os.path.getmtime(latest) > before_click
                and not latest.endswith(".crdownload")
            ):
                return latest
            attempts += 1
        return None
    except Exception as e:
        print(f"   > Abair Error: {e}")
        return None
