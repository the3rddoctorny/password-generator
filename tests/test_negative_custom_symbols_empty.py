import pytest
pytestmark = pytest.mark.negative

from selenium.webdriver.common.by import By


def test_custom_symbols_empty_does_not_break_generation(page, driver):
    # Symbols ON, custom set selected, but custom symbols empty.
    # App should still generate a password and not get stuck / crash.

    page.set_include_symbol(True)
    page.set_symbol_set("custom")
    page.set_custom_symbols("")

    page.generate()
    pwd = page.password()

    assert pwd.strip(), "Password should still generate even if custom symbols are empty"
    assert driver.find_element(By.ID, "generate").is_enabled(), "Generate should remain enabled"

