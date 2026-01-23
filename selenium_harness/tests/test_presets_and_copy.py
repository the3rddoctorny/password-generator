import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_preset_no_symbols_turns_symbols_off(page, driver):
    page.set_preset("noSymbols")
    # Generate a few times and ensure no symbol characters appear
    for _ in range(5):
        page.generate()
        pwd = page.password()
        assert not re.search(r"[!@\$\?\*\+\-=\.\_\-]", pwd), f"Unexpected symbol in: {pwd}"


def test_copy_shows_feedback_and_uses_test_clipboard(page, driver):
    page.set_mode("length").set_length(12).generate()
    pwd = page.password()
    assert pwd

    page.install_test_clipboard()
    page.copy()

    WebDriverWait(driver, 5).until(lambda d: "copied" in d.find_element(By.ID, "hint").text.lower())
    assert page.read_test_clipboard() == pwd
