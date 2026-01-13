from axe_selenium_python import Axe
from pages.password_generator_page import PasswordGeneratorPage

import json

def test_password_generator_accessibility(driver):
    page = PasswordGeneratorPage(driver).open()

    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    violations = results["violations"]

    with open("accessibility_baseline.json") as f:
        baseline = json.load(f)

    baseline_ids = {v["id"] for v in baseline}

    new_violations = [
        v for v in violations
        if v["id"] not in baseline_ids and v["impact"] in ("critical", "serious")
    ]

    assert not new_violations, summarize(new_violations)
