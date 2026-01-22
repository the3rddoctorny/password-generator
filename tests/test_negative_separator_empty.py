import pytest
pytestmark = pytest.mark.negative

from selenium.webdriver.common.by import By


def _set_separator(driver, value: str):
    # Use a direct element set to avoid brittle keystroke timing.
    sep = driver.find_element(By.ID, "separator")
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
        sep,
        value,
    )


def test_separator_empty_or_whitespace_does_not_break_generation(page, driver):
    # Separator only applies to "words" mode in most implementations.
    # If your page object uses a different mode setter, swap this call accordingly.
    page.set_mode("words")
    page.set_word_count(3)

    for bad_sep in ("", "   ", "\t"):
        _set_separator(driver, bad_sep)
        page.generate()
        pwd = page.password()

        assert pwd.strip(), f"Password should generate even with separator={repr(bad_sep)}"
        assert "undefined" not in pwd.lower(), "Should never leak 'undefined' into output"

