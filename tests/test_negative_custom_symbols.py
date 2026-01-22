import pytest
pytestmark = pytest.mark.negative

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_custom_symbols_empty_does_not_break_generation(page, driver):
    # Configure a "bad" but realistic state:
    # symbols enabled, custom symbol set selected, but no custom symbols provided.
    page.set_include_symbol(True)
    page.set_symbol_set("custom")
    page.set_custom_symbols("")

    # Generate should still produce a non-empty password (app should gracefully fall back / skip symbols)
    page.generate()
    pwd = page.password()
    assert pwd.strip(), "Password should still generate even if custom symbol set is empty"

    # Optional: ensure the UI didn't get stuck
    gen_btn = driver.find_element(By.ID, "generate")
    assert gen_btn.is_enabled(), "Generate button should remain enabled"

