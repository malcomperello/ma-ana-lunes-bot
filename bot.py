import os
import json
from playwright.sync_api import sync_playwright

USERNAME = os.environ["X_USERNAME"]
PASSWORD = os.environ["X_PASSWORD"]

STATE_FILE = "state.json"


def login_if_needed(page, context):
    print("🔐 Comprobando login...")

    page.goto("https://twitter.com/home", wait_until="domcontentloaded", timeout=60000)

    # Si ya estamos logueados, hay timeline
    if page.locator('div[data-testid="primaryColumn"]').count() > 0:
        print("✅ Ya logueado (sesión válida)")
        return

    print("❌ No hay sesión, haciendo login...")

    page.goto("https://twitter.com/login", wait_until="domcontentloaded", timeout=60000)

    # Debug por si X bloquea
    print("URL login:", page.url)

    # USERNAME STEP
    username_input = page.locator('input').first
    username_input.wait_for(state="attached", timeout=60000)
    username_input.fill(USERNAME)
    username_input.press("Enter")

    page.wait_for_timeout(3000)

    # PASSWORD STEP
    password_input = page.locator('input[name="password"]')
    password_input.wait_for(state="visible", timeout=60000)
    password_input.fill(PASSWORD)
    password_input.press("Enter")

    page.wait_for_timeout(8000)

    # Guardar sesión
    context.storage_state(path=STATE_FILE)
    print("💾 Sesión guardada")


def tweet(page):
    print("🐦 Abriendo composer...")

    page.goto("https://twitter.com/compose/tweet", wait_until="domcontentloaded", timeout=60000)

    box = page.locator('div[data-testid="tweetTextarea_0"]')
    box.wait_for(state="visible", timeout=60000)

    box.click()
    box.fill("SÍ.")

    page.wait_for_timeout(2000)

    print("📤 Enviando tweet...")

    page.locator('div[data-testid="tweetButtonInline"]').click()

    page.wait_for_timeout(5000)

    print("✅ Tweet enviado")


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled"
        ]
    )

    # Reusar sesión si existe
    if os.path.exists(STATE_FILE):
        context = browser.new_context(storage_state=STATE_FILE)
    else:
        context = browser.new_context()

    page = context.new_page()

    try:
        login_if_needed(page, context)
        tweet(page)

    except Exception as e:
        print("❌ ERROR:", str(e))
        page.screenshot(path="error.png")
        print("📸 Screenshot guardado: error.png")

    finally:
        context.close()
        browser.close()
