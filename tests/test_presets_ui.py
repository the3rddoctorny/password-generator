from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select


def _selected_value(select_el) -> str:
    return Select(select_el).first_selected_option.get_attribute("value")


def test_preset_no_symbols_flips_include_symbol_off(page, driver):
    page.set_preset("noSymbols")

    include_symbol = driver.find_element(By.ID, "includeSymbol")
    WebDriverWait(driver, 5).until(lambda d: include_symbol.is_selected() is False)
    assert include_symbol.is_selected() is False


def test_preset_letters_only_flips_digit_and_symbol_off(page, driver):
    page.set_preset("lettersOnly")

    include_digit = driver.find_element(By.ID, "includeDigit")
    include_symbol = driver.find_element(By.ID, "includeSymbol")

    WebDriverWait(driver, 5).until(lambda d: include_digit.is_selected() is False)
    WebDriverWait(driver, 5).until(lambda d: include_symbol.is_selected() is False)

    assert include_digit.is_selected() is False
    assert include_symbol.is_selected() is False


def test_preset_alnum_flips_digit_on_symbol_off(page, driver):
    page.set_preset("alnum")

    include_digit = driver.find_element(By.ID, "includeDigit")
    include_symbol = driver.find_element(By.ID, "includeSymbol")

    WebDriverWait(driver, 5).until(lambda d: include_digit.is_selected() is True)
    WebDriverWait(driver, 5).until(lambda d: include_symbol.is_selected() is False)

    assert include_digit.is_selected() is True
    assert include_symbol.is_selected() is False

