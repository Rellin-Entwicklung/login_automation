# notion selenium - Verbesserte Version
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Lade Umgebungsvariablen
load_dotenv()

NOTION_EMAIL = os.getenv("NOTION_EMAIL")
NOTION_PASSWORD = os.getenv("PW")


def notion_login():
    # Chrome Optionen
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")

    # Browser starten
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 15)

    try:
        print("Öffne Notion Login...")
        driver.get("https://www.notion.so/login")
        time.sleep(2)

        # SCHRITT 1: E-Mail eingeben
        print("Suche E-Mail Feld...")
        email_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        email_field.clear()
        email_field.send_keys(NOTION_EMAIL)
        print(f"E-Mail eingegeben: {NOTION_EMAIL}")
        time.sleep(1)

        # Mit Enter bestätigen (zuverlässiger als Button-Klick)
        email_field.send_keys(Keys.RETURN)
        print("E-Mail mit Enter bestätigt.")
        time.sleep(3)

        # SCHRITT 2: Passwort eingeben
        print("Suche Passwort Feld...")
        password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        password_field.clear()
        password_field.send_keys(NOTION_PASSWORD)
        print("Passwort eingegeben.")
        time.sleep(1)

        # Passwort mit Enter bestätigen
        password_field.send_keys(Keys.RETURN)
        print("Passwort mit Enter bestätigt.")

        # SCHRITT 3: Warten auf erfolgreichen Login
        print("Warte auf erfolgreichen Login...")
        time.sleep(5)

        # Prüfe, ob Login erfolgreich war (URL ändert sich)
        if "login" not in driver.current_url.lower():
            print(f"✓ Login erfolgreich! Aktuelle URL: {driver.current_url}")
        else:
            print("⚠ Login-Seite noch aktiv. Bitte manuell prüfen.")

            # Versuche alternativen Button-Klick
            try:
                print("Versuche Login-Button zu finden...")
                # Verschiedene mögliche Selektoren
                selectors = [
                    "//button[contains(text(), 'Continue')]",
                    "//button[@type='submit']",
                    "//div[@role='button' and contains(., 'Continue')]",
                    "//button[contains(@class, 'notion')]"
                ]

                for selector in selectors:
                    try:
                        button = driver.find_element(By.XPATH, selector)
                        button.click()
                        print(f"Button gefunden und geklickt: {selector}")
                        time.sleep(3)
                        break
                    except:
                        continue

            except Exception as e:
                print(f"Button-Klick fehlgeschlagen: {e}")

        print("\nScript abgeschlossen. Browser bleibt offen.")

    except Exception as e:
        print(f"Fehler aufgetreten: {e}")
        print(f"Aktuelle URL: {driver.current_url}")
        # Screenshot für Debugging
        try:
            driver.save_screenshot("notion_login_error.png")
            print("Screenshot gespeichert: notion_login_error.png")
        except:
            pass


if __name__ == "__main__":
    if not NOTION_EMAIL or not NOTION_PASSWORD:
        print("FEHLER: NOTION_EMAIL oder PW nicht in .env gefunden!")
    else:
        notion_login()