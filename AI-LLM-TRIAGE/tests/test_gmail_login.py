import pytest
from playwright.sync_api import expect

@pytest.mark.asyncio
async def test_gmail_login(page):
    # Navigate to Gmail login page
    await page.goto("https://mail.google.com")
    
    # Enter email
    await page.fill("input#identifierId", "test.user@gmail.com")  # Placeholder email
    await page.click("button >> text=Next")
    
    # Enter password
    await page.wait_for_selector("input[name='Passwd']", timeout=10000)
    await page.fill("input[name='Passwd']", "testpassword")  # Placeholder password
    await page.click("button >> text=Next")
    
    # Assert Gmail logo is visible after login
    await page.wait_for_selector("img[alt='Gmail']", timeout=10000)
    expect(page.locator("img[alt='Gmail']")).to_be_visible()
