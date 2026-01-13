from axe_selenium_python import Axe
from pages.password_generator_page import PasswordGeneratorPage

def test_password_generator_accessibility(driver):
    page = PasswordGeneratorPage(driver).open()

    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    violations = results["violations"]

    assert violations == [], f"Accessibility violations found: {violations}"

