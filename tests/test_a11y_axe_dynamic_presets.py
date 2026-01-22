import pytest
pytestmark = pytest.mark.a11y

from test_a11y_axe import run_axe, format_violations  # adjust import if needed


def test_a11y_after_preset_toggle_has_no_wcag_a_aa_violations(page, driver):
    # Flip some UI state that could introduce issues (labels, contrast, aria updates, etc.)
    page.set_preset("strict")  # change to an existing preset id if yours differs
    page.generate()

    violations = run_axe(driver, test_name="after_preset_toggle", tags=["wcag2a", "wcag2aa"])
    assert not violations, "Accessibility violations found:\n" + format_violations(violations)

