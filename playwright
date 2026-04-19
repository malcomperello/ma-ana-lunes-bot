import os
from playwright.sync_api import sync_playwright

USERNAME = os.environ["X_USERNAME"]
PASSWORD = os.environ["X_PASSWORD"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1. Login
    page.goto("https://twitter.com/login")

    page.fill('input[name="text"]', USERNAME)
    page.click('text=Next')

    page.wait_for_timeout(2000)

    # a veces pide username otra vez
    if page.locator('input[name="text"]').count() > 0:
        page.fill('input[name="text"]', USERNAME)
        page.click('text=Next')

    page.fill('input[name="password"]', PASSWORD)
    page.click('text=Log in')

    page.wait_for_timeout(5000)

    # 2. Ir a tweet
    page.goto("https://twitter.com/compose/tweet")

    page.fill('div[data-testid="tweetTextarea_0"]', "SÍ.")
    page.click('div[data-testid="tweetButtonInline"]')

    page.wait_for_timeout(3000)

    print("Tweet enviado")
    browser.close()
