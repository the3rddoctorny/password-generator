import pytest
pytestmark = pytest.mark.a11y

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from test_a11y_axe import run_axe, format_violations  # adjust import if your file name differs


def test_a11y_history_populated_has_no_wcag_a_aa_violations(page, driver):
    # Populate history so extra UI appears
    driver.find_element(By.ID, "clearHistory").click()
    page.set_batch_count(5).generate()

    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) >= 3
    )

    violations = run_axe(driver, test_name="history_populated", tags=["wcag2a", "wcag2aa"])
    assert not violations, "Accessibility violations found:\n" + format_violations(violations)

