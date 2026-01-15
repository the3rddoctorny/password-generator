from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordGeneratorPage:
    URL = "https://the3rddoctorny.github.io/password-generator/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self):
        self.driver.get(self.URL)

        # Basic sanity: the UI is present
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.wait.until(EC.presence_of_element_located((By.ID, "generate")))

        # If your JS didn't define the flags, stop pretending and fail loudly.
        has_flags = self.driver.execute_script("""
            return (typeof window.__wordsLoaded !== 'undefined')
                && (typeof window.__wordsLoadError !== 'undefined');
        """)

        if not has_flags:
            # Grab console logs if available (Chrome usually supports this)
            logs = []
            try:
                for entry in self.driver.get_log("browser"):
                    logs.append(f"{entry.get('level')}: {entry.get('message')}")
            except Exception:
                logs.append("(Could not read browser console logs)")

            snippet = self.driver.page_source[:500]
            raise AssertionError(
                "Page does not expose wordlist flags (__wordsLoaded/__wordsLoadError).\n"
                "That means your index.html was not updated or the deployed page is stale.\n\n"
                f"TITLE: {self.driver.title}\n"
                f"URL: {self.driver.current_url}\n\n"
                "BROWSER LOGS:\n" + "\n".join(logs[-10:]) + "\n\n"
                "HTML SNIPPET:\n" + snippet
            )

        # Wait for loaded OR fail with the error string
        def words_ready(d):
            loaded = d.execute_script("return window.__wordsLoaded === true;")
            if loaded:
                return True
            err = d.execute_script("return window.__wordsLoadError || '';")
            if err:
                raise AssertionError(f"Wordlist failed to load: {err}")
            return False

        self.wait.until(words_ready)
        return self

    def set_length(self, length: int):
        sel = self.driver.find_element(By.ID, "length")
        sel.send_keys(str(length))
        return self

    def generate(self):
        # Clear previous value so we can wait for a change
        self.driver.execute_script("document.getElementById('password').textContent = '';")
        self.driver.find_element(By.ID, "generate").click()

        self.wait.until(lambda d: d.find_element(By.ID, "password").text.strip() != "")
        return self

    def password(self):
        return self.driver.find_element(By.ID, "password").text.strip()

    def copy(self):
        self.driver.find_element(By.ID, "copy").click()
        return self

