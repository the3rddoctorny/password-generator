import pytest
pytestmark = pytest.mark.a11y

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_help_modal_focus_and_escape_close(page, driver):
    # Open Help
    driver.find_element(By.ID, "helpBtn").click()

    overlay = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "helpOverlay"))
    )

    # Focus should move into the modal (or at least be inside the overlay)
    def focus_inside_modal(d):
        active = d.switch_to.active_element
        return d.execute_script(
            "return arguments[0].contains(arguments[1]);", overlay, active
        )

    WebDriverWait(driver, 5).until(focus_inside_modal)

    # Esc should close the modal
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "helpOverlay")))

