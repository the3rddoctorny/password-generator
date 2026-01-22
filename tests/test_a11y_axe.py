import pytest
pytestmark = pytest.mark.a11y

import json
from pathlib import Path

import pytest
from axe_selenium_python import Axe
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def run_axe(driver, *, test_name: str, tags=None):
    axe = Axe(driver)
    axe.inject()

    # Focus on WCAG A/AA checks (keeps noise down)
    options = {}
    if tags:
        options["runOnly"] = {"type": "tag", "values": tags}

    results = axe.run(options=options)

    # Save results for debugging when something fails
    out = Path("axe-results")
    out.mkdir(exist_ok=True)
    (out / f"{test_name}.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    violations = results.get("violations", [])
    return violations


def format_violations(violations):
    lines = []
    for v in violations:
        lines.append(f"- {v.get('id')} ({', '.join(v.get('tags', []))})")
        lines.append(f"  {v.get('help')}")
        for node in v.get("nodes", [])[:5]:
            target = " ".join(node.get("target", []))
            lines.append(f"    • {target}")
    return "\n".join(lines)


def test_a11y_home_page_has_no_wcag_a_aa_violations(page, driver):
    violations = run_axe(driver, test_name="home", tags=["wcag2a", "wcag2aa"])
    assert not violations, "Accessibility violations found:\n" + format_violations(violations)


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_a11y_help_modal_has_no_wcag_a_aa_violations(page, driver):
    driver.find_element(By.ID, "helpBtn").click()

    # Wait until the overlay is actually visible (instead of relying on aria-hidden)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "helpOverlay"))
    )

    violations = run_axe(driver, test_name="help_modal", tags=["wcag2a", "wcag2aa"])
    assert not violations, "Accessibility violations found:\n" + format_violations(violations)

