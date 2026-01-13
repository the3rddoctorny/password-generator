from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordGeneratorPage:
    URL = Path(__file__).resolve().parents[1] / "index.html"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL.as_uri())

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "length"))
        )

        return self

    def set_length(self, length: int):
        select = self.driver.find_element(By.ID, "length")
        select.send_keys(str(length))
        return self

    def generate(self):
        self.driver.find_element(By.ID, "generate").click()
        return self

    def password(self):
        return self.driver.find_element(By.ID, "password").text

    def copy(self):
        self.driver.find_element(By.ID, "copy").click()
        return self

