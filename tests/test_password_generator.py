import re
import pytest
from pages.password_generator_page import PasswordGeneratorPage

AMBIGUOUS = set("I0O")
SYMBOLS = set("*+-=?!@$")

@pytest.mark.parametrize(
    "length",
    [8, 12, 15],
    ids=["len8", "len12", "len15"]
)
def test_password_rules(driver, length):
    page = PasswordGeneratorPage(driver).open()
    page.set_length(length).generate()

    pwd = page.password()

    # Exact length
    assert len(pwd) == length, f"Expected {length}, got {len(pwd)}: {pwd}"

    # Required classes
    assert re.search(r"[A-Z]", pwd), f"No uppercase in {pwd}"
    assert re.search(r"[0-9]", pwd), f"No number in {pwd}"
    assert any(c in SYMBOLS for c in pwd), f"No symbol in {pwd}"

    # No ambiguous characters
    assert not any(c in AMBIGUOUS for c in pwd), f"Ambiguous char in {pwd}"

