import pytest
from playwright.sync_api import Page, expect

def test_gmail_login(page: Page):
    page.goto("https://mail.google.com")

    page.fill("input#identifierId", "test.user@gmail.com")  # Placeholder email
    page.click("button:has-text('Next')")

    page.wait_for_selector("input[name='Passwd']", timeout=10000)
    page.fill("input[name='Passwd']", "testpassword")  # Placeholder password
    page.click("button:has-text('Next')")

    page.wait_for_selector("img[alt='Gmail']", timeout=10000)
    expect(page.locator("img[alt='Gmail']")).to_be_visible()
