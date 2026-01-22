import pytest
pytestmark = pytest.mark.smoke

def test_page_loads_and_generates(page):
    page.generate()
    assert page.password() != ""
