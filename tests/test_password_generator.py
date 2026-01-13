import re
import pytest
from pages.password_generator_page import PasswordGeneratorPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

AMBIGUOUS = set("I0O")
SYMBOLS = set("*+-=?!@$")

@pytest.mark.parametrize(
    "length",
    [8, 12, 15],
    ids=["len8", "len12", "len15"]
)
def test_password_rules(driver, length):
    page = PasswordGeneratorPage(driver).open()
    page.set_length(length).generate()

    pwd = page.password()

    # Exact length
    assert len(pwd) == length, f"Expected {length}, got {len(pwd)}: {pwd}"

    # Required classes
    assert re.search(r"[A-Z]", pwd), f"No uppercase in {pwd}"
    assert re.search(r"[0-9]", pwd), f"No number in {pwd}"
    assert any(c in SYMBOLS for c in pwd), f"No symbol in {pwd}"

    # No ambiguous characters
    assert not any(c in AMBIGUOUS for c in pwd), f"Ambiguous char in {pwd}"

def test_password_rules_hold_across_multiple_generations(driver):
    page = PasswordGeneratorPage(driver).open()

    for length in (8, 12, 15):
        page.set_length(length)

        for _ in range(20):  # 20 random generations per length
            page.generate()
            pwd = page.password()

            assert len(pwd) == length, f"Length mismatch: {pwd}"
            assert re.search(r"[A-Z]", pwd), f"No uppercase: {pwd}"
            assert re.search(r"[0-9]", pwd), f"No number: {pwd}"
            assert any(c in SYMBOLS for c in pwd), f"No symbol: {pwd}"
            assert not any(c in AMBIGUOUS for c in pwd), f"Ambiguous char: {pwd}"

def test_copy_button_shows_feedback(driver):
    page = PasswordGeneratorPage(driver).open()
    page.set_length(12).generate()

    pwd = page.password()
    assert pwd, "Password should exist before copying"

    page.copy()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "hint"), "Copied!")
)

import pytest

@pytest.mark.skip(reason="Clipboard access unreliable in headless browsers")
def test_copy_button_copies_password_to_clipboard(driver):
    page = PasswordGeneratorPage(driver).open()
    page.set_length(12).generate()

    pwd = page.password()
    page.copy()

    copied = driver.execute_async_script("""
        const done = arguments[0];
        navigator.clipboard.readText()
            .then(text => done(text))
            .catch(() => done(null));
    """)

    assert copied == pwd, f"Clipboard mismatch: expected {pwd}, got {copied}"

