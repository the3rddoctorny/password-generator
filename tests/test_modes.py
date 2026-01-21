import re


def test_exact_length_mode_respects_length(page):
    page.set_mode("length").set_length(12).generate()
    pwd = page.password()
    assert len(pwd) == 12


def test_word_count_mode_separator_title_case(page):
    # Make this deterministic-ish: no digit/symbol so the word split is clean
    page.set_mode("words")
    page.set_include_digit(False)
    page.set_include_symbol(False)
    page.set_word_count(3).set_separator("-").set_title_case(True)
    page.generate()
    pwd = page.password()

    parts = pwd.split("-")
    assert len(parts) == 3, f"Expected 3 words separated by '-', got: {pwd}"
    assert all(re.match(r"^[A-Z][a-z]+$", w) for w in parts), f"Expected Title Case words, got: {pwd}"
