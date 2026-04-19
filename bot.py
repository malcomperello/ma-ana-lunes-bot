import os
from playwright.sync_api import sync_playwright

USERNAME = os.environ["X_USERNAME"]
PASSWORD = os.environ["X_PASSWORD"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Abriendo login...")
    page.goto("https://twitter.com/login", timeout=60000)

    # Esperar a que cargue el input
    page.wait_for_selector('input', timeout=60000)

    print("Escribiendo usuario...")
    page.get_by_placeholder("Phone, email, or username").fill(USERNAME)
    page.keyboard.press("Enter")

    page.wait_for_timeout(5000)

    # Por si pide username otra vez
    if page.locator('input').count() > 0:
        try:
            page.get_by_placeholder("Phone, email, or username").fill(USERNAME)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)
        except:
            pass

    print("Escribiendo contraseña...")
    page.get_by_label("Password").fill(PASSWORD)
    page.keyboard.press("Enter")

    page.wait_for_timeout(8000)

    print("Yendo a escribir tweet...")
    page.goto("https://twitter.com/compose/tweet", timeout=60000)

    page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=60000)

    print("Escribiendo tweet...")
    page.fill('div[data-testid="tweetTextarea_0"]', "SÍ.")

    page.wait_for_timeout(2000)

    print("Enviando tweet...")
    page.click('div[data-testid="tweetButtonInline"]')

    page.wait_for_timeout(5000)

    print("✅ Tweet enviado")
    browser.close()
