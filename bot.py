import os
from playwright.sync_api import sync_playwright

USERNAME = os.environ["X_USERNAME"]
PASSWORD = os.environ["X_PASSWORD"]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page()

    print("Abriendo login...")

    # Mejor esperar carga real del DOM (Better wait for DOM load)
    page.goto("https://twitter.com/login", wait_until="domcontentloaded", timeout=60000)

    # =========================
    # LOGIN - USERNAME
    # =========================
    print("Escribiendo usuario...")

    username_input = page.locator('input[autocomplete="username"]')
    username_input.wait_for(state="visible", timeout=60000)
    username_input.fill(USERNAME)
    username_input.press("Enter")

    page.wait_for_timeout(3000)

    # =========================
    # LOGIN - POSSIBLE SECOND STEP (fallback)
    # =========================
    # (A veces X pide username otra vez o teléfono - Sometimes X asks again)

    try:
        extra_input = page.locator('input[autocomplete="username"]')
        if extra_input.count() > 0 and extra_input.is_visible():
            extra_input.fill(USERNAME)
            extra_input.press("Enter")
            page.wait_for_timeout(3000)
    except:
        pass

    # =========================
    # LOGIN - PASSWORD
    # =========================
    print("Escribiendo contraseña...")

    password_input = page.locator('input[name="password"]')
    password_input.wait_for(state="visible", timeout=60000)
    password_input.fill(PASSWORD)
    password_input.press("Enter")

    page.wait_for_timeout(8000)

    # =========================
    # GO TO TWEET COMPOSER
    # =========================
    print("Yendo a escribir tweet...")

    page.goto("https://twitter.com/compose/tweet", wait_until="domcontentloaded", timeout=60000)

    tweet_box = page.locator('div[data-testid="tweetTextarea_0"]')
    tweet_box.wait_for(state="visible", timeout=60000)

    # =========================
    # WRITE TWEET
    # =========================
    print("Escribiendo tweet...")

    tweet_box.click()
    tweet_box.fill("SÍ.")

    page.wait_for_timeout(2000)

    # =========================
    # SEND TWEET
    # =========================
    print("Enviando tweet...")

    send_button = page.locator('div[data-testid="tweetButtonInline"]')
    send_button.wait_for(state="visible", timeout=60000)
    send_button.click()

    page.wait_for_timeout(5000)

    print("✅ Tweet enviado")
    browser.close()
