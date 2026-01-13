import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def driver():
    options = Options()

    # CI / headless safe defaults
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

