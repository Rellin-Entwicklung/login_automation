# notion selenium
# funktioniert wegen der notion dynamik (andere login-seiten) nicht
# --- KONFIGURATION ---

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
NOTION_EMAIL = "test"
NOTION_PW = "PW"


def notion_login_mit_klick():
    # Setup Chrome Optionen (mit Detach, um den Browser offen zu halten)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # Browser starten
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Warteobjekt
    wait = WebDriverWait(driver, 10)

    try:
        print("Öffne Notion Login...")
        driver.get("https://www.notion.so/login")

        # --- SCHRITT 1: E-Mail eingeben und weiter ---

        # 1. E-Mail Feld finden
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_field.send_keys(NOTION_EMAIL)
        print("E-Mail eingegeben.")

        # 2. Den "Weiter"-Button finden und klicken
        # Notion nutzt oft Buttons mit dem Text "Continue with email" oder "Weiter mit E-Mail"
        # Wir suchen einen Button mit dem Text "Weiter" oder "Continue"

        # ACHTUNG: Der Login-Button im ersten Schritt hat meistens die Rolle "button"
        # und keinen sichtbaren Text, aber wir versuchen es über den Text oder die Rolle.

        # Versuchen wir, den Button direkt nach der Eingabe zu klicken:
        # Der Button befindet sich oft in einem div oder hat eine spezifische Klasse.
        # Am stabilsten ist es oft, den Button zu suchen, der das Attribut 'type="submit"' hat
        # oder den Text 'Continue' / 'Weiter' enthält.

        # Versuchs-Selector für den "Weiter"-Button (kann variieren):
        # Der Button ist oft das 'button' Element, das als 'submit' fungiert.

        try:
            # Versuche, den Submit-Button im E-Mail-Formular zu finden und zu klicken
            continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button']")))
            continue_button.click()
            print("Auf 'Weiter/Continue' geklickt.")
        except:
            # Wenn der Klick nicht funktioniert, versuchen wir es wieder mit Enter
            email_field.send_keys(Keys.RETURN)
            print("Klick fehlgeschlagen, stattdessen 'Enter' für E-Mail verwendet.")

        # --- SCHRITT 2: Passwort eingeben und Login-Button klicken ---

        # 3. Passwort Feld finden (warten, bis es im DOM erscheint)
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(NOTION_PW)
        print("Passwort eingegeben.")

        # 4. Den finalen LOGIN-Button finden und klicken
        # Wir suchen erneut den Button mit der Rolle 'button'
        # Dieser erscheint erst, nachdem das Passwortfeld geladen wurde.
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button']")))
        login_button.click()
        print("Auf 'Login' geklickt. Prozess abgeschlossen.")

        # Optional: Warten auf die Startseite
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notion-sidebar")))
        # print("Erfolgreich eingeloggt!")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        # driver.quit() # Entkommentieren, wenn Browser bei Fehler geschlossen werden soll


if __name__ == "__main__":
    notion_login_mit_klick()