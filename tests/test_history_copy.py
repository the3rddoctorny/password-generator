from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_copy_from_history_uses_test_clipboard(page, driver):
    # Ensure empty history
    driver.find_element(By.ID, "clearHistory").click()
    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) == 0
    )

    # Generate one item so we have history
    page.set_batch_count(1).generate()

    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) == 1
    )

    # Install stable clipboard shim
    page.install_test_clipboard()

    # Grab first history password text
    first_item = driver.find_element(By.CSS_SELECTOR, "#historyList > li.historyItem")
    hist_pwd = first_item.find_element(By.CSS_SELECTOR, ".historyPwd").text.strip()
    assert hist_pwd, "Expected a history password"

    # Click the Copy button inside that history row
    buttons = first_item.find_elements(By.CSS_SELECTOR, "button")
    copy_btn = next(b for b in buttons if b.text.strip().lower() == "copy")
    copy_btn.click()

    # Wait for "Copied!" feedback
    WebDriverWait(driver, 5).until(
        lambda d: "copied" in d.find_element(By.ID, "hint").text.lower()
    )

    # Verify it used the shim clipboard
    assert page.read_test_clipboard() == hist_pwd

