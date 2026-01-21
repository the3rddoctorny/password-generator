from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_batch_generates_exact_history_count_after_clear(page, driver):
    # Clear history first so we can be strict about the count
    driver.find_element(By.ID, "clearHistory").click()

    # Confirm empty (history items are li.historyItem)
    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) == 0
    )

    # Batch 5 should create exactly 5 history items
    page.set_batch_count(5).generate()

    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) == 5
    )

