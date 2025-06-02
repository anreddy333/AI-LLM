import pytest

# Function to check if a number is even or odd
def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Test case for even numbers
def test_even():
    result = check_even_odd(4)
    print(f"Testing check_even_odd(4): {result}")
    assert result == "Even"

    result = check_even_odd(0)
    print(f"Testing check_even_odd(0): {result}")
    assert result == "Even"

    result = check_even_odd(-2)
    print(f"Testing check_even_odd(-2): {result}")
    assert result == "Even"

# Test case for odd numbers
def test_odd():
    result = check_even_odd(3)
    print(f"Testing check_even_odd(3): {result}")
    assert result == "Odd"

    result = check_even_odd(7)
    print(f"Testing check_even_odd(7): {result}")
    assert result == "Odd"

    result = check_even_odd(-5)
    print(f"Testing check_even_odd(-5): {result}")
    assert result == "Odd"

# Running the tests
if __name__ == "__main__":
    pytest.main()


import pytest
from playwright.sync_api import Page, expect


def test_gmail_login_success(page: Page):
    page.goto("https://mail.google.com")
    
    page.fill("input#identifierId", "test.sds0003@gmail.com")
    page.click("//span[normalize-space()='Next']")
    
    page.wait_for_selector("input[name='Passwd']", timeout=10000)
    page.fill("input[name='Passwd']", "test@0003")  
    page.click("//span[normalize-space()='Next']")
    
    page.wait_for_selector("img[alt='Gmail']", timeout=10000)
    expect(page.locator("img[alt='Gmail']")).to_be_visible()

def test_forgot_email_link(page: Page):
    page.goto("https://mail.google.com")

    forgot_email = page.locator("//button[normalize-space()='Forgot email?']")
    expect(forgot_email).to_be_visible()    
    forgot_email.click()
    
def test_create_account_link(page: Page):
    page.goto("https://mail.google.com")
    
    create_account_link = page.locator("//span[normalize-space()='Create account']")
    expect(create_account_link).to_be_visible()
    create_account_link.click()
