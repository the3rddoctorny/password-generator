from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_export_history_csv_contains_all_items(page, driver):
    # Start clean so counts are strict
    driver.find_element(By.ID, "clearHistory").click()
    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) == 0
    )

    # Generate 5 items into history
    page.set_batch_count(5).generate()
    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#historyList > li.historyItem")) == 5
    )

    # Install an export capture shim (no real download needed)
    driver.execute_script(
        """
        window.__exportCapture = { blob: null, filename: null, href: null };

        URL.__origCreateObjectURL = URL.__origCreateObjectURL || URL.createObjectURL;
        URL.__origRevokeObjectURL = URL.__origRevokeObjectURL || URL.revokeObjectURL;
        HTMLAnchorElement.prototype.__origClick = HTMLAnchorElement.prototype.__origClick || HTMLAnchorElement.prototype.click;

        URL.createObjectURL = function(blob){
          window.__exportCapture.blob = blob;
          return "blob:captured";
        };
        URL.revokeObjectURL = function(url){ /* no-op for test */ };

        HTMLAnchorElement.prototype.click = function(){
          window.__exportCapture.href = this.href;
          window.__exportCapture.filename = this.download;
          // do NOT navigate
        };
        """
    )

    # Click Export
    driver.find_element(By.ID, "exportHistory").click()

    # Pull captured CSV text from the Blob
    result = driver.execute_async_script(
        """
        const done = arguments[arguments.length - 1];
        (async () => {
          const cap = window.__exportCapture || {};
          if (!cap.blob) return done({ ok: false, err: "No blob captured" });

          const text = await cap.blob.text();
          done({ ok: true, text, filename: cap.filename, href: cap.href });
        })();
        """
    )

    assert result["ok"], result.get("err", "Export capture failed")

    csv = result["text"]
    filename = result["filename"] or ""

    # Filename sanity
    assert filename.startswith("password_history_")
    assert filename.endswith(".csv")

    # CSV structure sanity
    lines = [line for line in csv.splitlines() if line.strip()]
    assert lines[0] == "index,password"

    # Expect 1 header + 5 rows
    assert len(lines) == 1 + 5

    # Each row should look like: 1,something
    for i, line in enumerate(lines[1:], start=1):
        assert line.startswith(f"{i},"), f"Row {i} malformed: {line}"

