from __future__ import annotations

from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class PasswordGeneratorPage:
    driver: WebDriver
    base_url: str
    timeout: int = 10

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, self.timeout)

    def open(self) -> "PasswordGeneratorPage":
        self.driver.get(self.base_url)
        self.wait.until(EC.presence_of_element_located((By.ID, "generate")))
        self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        return self

    # ---------- helpers ----------
    def _select(self, el_id: str, value: str) -> None:
        el = self.driver.find_element(By.ID, el_id)
        Select(el).select_by_value(value)

    def _set_checkbox(self, el_id: str, desired: bool) -> None:
        el = self.driver.find_element(By.ID, el_id)
        if el.is_selected() != desired:
            el.click()

    def wait_ready(self) -> "PasswordGeneratorPage":
        # Your app disables the Generate button and shows "Loading…" until words are ready (or fallback is ready).
        def _is_ready(d: WebDriver) -> bool:
            btn = d.find_element(By.ID, "generate")
            text_ok = btn.text.strip().lower().startswith("generate")
            enabled = btn.is_enabled() and btn.get_attribute("disabled") is None
            return text_ok and enabled

        self.wait.until(_is_ready)
        return self

    # ---------- interactions ----------
    def set_mode(self, mode: str) -> "PasswordGeneratorPage":
        # mode: "length" or "words"
        self._select("mode", mode)
        return self

    def set_length(self, length: int) -> "PasswordGeneratorPage":
        self._select("length", str(length))
        return self

    def set_word_count(self, n: int) -> "PasswordGeneratorPage":
        self._select("wordCount", str(n))
        return self

    def set_separator(self, sep: str) -> "PasswordGeneratorPage":
        # sep: "", "-", "_", "."
        self._select("separator", sep)
        return self

    def set_title_case(self, enabled: bool) -> "PasswordGeneratorPage":
        self._set_checkbox("titleCase", enabled)
        return self

    def set_include_digit(self, enabled: bool) -> "PasswordGeneratorPage":
        self._set_checkbox("includeDigit", enabled)
        return self

    def set_include_symbol(self, enabled: bool) -> "PasswordGeneratorPage":
        self._set_checkbox("includeSymbol", enabled)
        return self

    def set_symbol_set(self, value: str) -> "PasswordGeneratorPage":
        # value: "basic" | "extended" | "custom"
        self._select("symbolSet", value)
        return self

    def set_custom_symbols(self, symbols: str) -> "PasswordGeneratorPage":
        el = self.driver.find_element(By.ID, "customSymbols")
        el.clear()
        el.send_keys(symbols)
        return self

    def set_preset(self, value: str) -> "PasswordGeneratorPage":
        # value: default|noSymbols|noDigits|alnum|lettersOnly|strict|custom
        self._select("preset", value)
        return self

    def set_batch_count(self, n: int) -> "PasswordGeneratorPage":
        self._select("batchCount", str(n))
        return self

    def generate(self) -> "PasswordGeneratorPage":
        self.driver.find_element(By.ID, "generate").click()
        # wait until password text is non-empty
        self.wait.until(lambda d: d.find_element(By.ID, "password").text.strip() != "")
        return self

    def password(self) -> str:
        return self.driver.find_element(By.ID, "password").text.strip()

    def hint(self) -> str:
        return self.driver.find_element(By.ID, "hint").text.strip()

    def strength(self) -> str:
        return self.driver.find_element(By.ID, "strength").text.strip()

    def copy(self) -> "PasswordGeneratorPage":
        self.driver.find_element(By.ID, "copy").click()
        return self

    def install_test_clipboard(self) -> None:
        # Your app prefers window.__testClipboard.writeText if present.
        self.driver.execute_script(
            """
            window.__testClipboard = {
              value: "",
              writeText: async function(t){ this.value = t; }
            };
            """
        )

    def read_test_clipboard(self) -> str:
        return self.driver.execute_script("return window.__testClipboard && window.__testClipboard.value || '';")

    def history_count(self) -> int:
        return len(self.driver.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem"))
