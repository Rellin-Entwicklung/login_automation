# notion selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- KONFIGURATION ---
NOTION_EMAIL = "deine_email@beispiel.com"
NOTION_PW = "dein_passwort"


def notion_login():
    # Setup Chrome Optionen
    chrome_options = Options()

    # WICHTIG: Diese Option sorgt dafür, dass der Browser offen bleibt,
    # wenn das Skript fertig ist. Sonst schließt sich Chrome sofort wieder.
    chrome_options.add_experimental_option("detach", True)

    # Browser starten (installiert den Treiber automatisch falls nötig)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # "wait" Objekt erstellen: Wartet max. 10 Sekunden auf Elemente
    wait = WebDriverWait(driver, 10)

    try:
        print("Öffne Notion Login...")
        driver.get("https://www.notion.so/login")

        # 1. E-Mail Feld finden und ausfüllen
        # Wir warten, bis ein Input-Feld mit type='email' sichtbar ist
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_field.send_keys(NOTION_EMAIL)
        email_field.send_keys(Keys.RETURN)  # Enter drücken

        print("E-Mail eingegeben.")

        # 2. Passwort Feld finden und ausfüllen
        # Notion lädt jetzt kurz. Selenium wartet automatisch, bis das Passwortfeld da ist.
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(NOTION_PW)
        password_field.send_keys(Keys.RETURN)  # Enter drücken

        print("Passwort eingegeben. Login läuft...")

        # Optional: Warten bis die Seite wirklich geladen ist (z.B. Sidebar sichtbar)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notion-sidebar")))
        # print("Erfolgreich eingeloggt!")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        # driver.quit() # Nur einkommentieren, wenn Browser bei Fehler schließen soll


if __name__ == "__main__":
    notion_login()