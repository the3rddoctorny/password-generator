from __future__ import annotations

import os
import socket
import threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.password_generator_page import PasswordGeneratorPage


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url() -> str:
    # Serve the repo root so index.html and assets/ are accessible.
    repo_root = Path(__file__).resolve().parents[1]
    port = _free_port()

    handler = partial(SimpleHTTPRequestHandler, directory=str(repo_root))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}/"

    httpd.shutdown()
    httpd.server_close()


@pytest.fixture()
def driver():
    headless = os.getenv("HEADLESS", "1") != "0"

    opts = Options()
    if headless:
        # "new" headless is less weird about focus/clipboard timing
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1200,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(options=opts)
    d.set_page_load_timeout(20)
    yield d
    d.quit()


@pytest.fixture()
def page(driver, base_url):
    p = PasswordGeneratorPage(driver, base_url).open().wait_ready()
    return p
