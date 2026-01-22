import pytest
pytestmark = pytest.mark.a11y

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_help_modal_tab_stays_within_modal(page, driver):
    driver.find_element(By.ID, "helpBtn").click()

    overlay = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "helpOverlay"))
    )

    # Press Tab a bunch of times and assert focus never leaves the overlay
    for _ in range(15):
        driver.switch_to.active_element.send_keys(Keys.TAB)

        active = driver.switch_to.active_element
        inside = driver.execute_script(
            "return arguments[0].contains(arguments[1]);", overlay, active
        )
        assert inside, "Focus escaped the help modal while tabbing"

