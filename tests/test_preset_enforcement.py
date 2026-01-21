import re


def test_preset_no_digits_never_generates_digits(page):
    page.set_preset("noDigits")

    for _ in range(15):
        page.generate()
        pwd = page.password()
        assert not re.search(r"\d", pwd), f"Unexpected digit in: {pwd}"

