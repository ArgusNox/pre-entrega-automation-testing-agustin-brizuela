"""Configuracion y fixtures que usan las pruebas."""

import logging
import os
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BASE_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com/")
USERNAME = os.getenv("SAUCEDEMO_USER", "standard_user")
PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
EVIDENCE_DIR = Path("reports") / "evidencias"
Path("reports").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("reports/execution.log", encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def _build_driver():
    """Abre Chrome. Por defecto corre sin mostrar la ventana."""
    options = Options()
    if os.getenv("HEADLESS", "true").lower() not in {"0", "false", "no"}:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    browser = _build_driver()
    browser.implicitly_wait(0)
    logger.info("Navegador iniciado")
    yield browser
    logger.info("Navegador finalizado")
    browser.quit()


@pytest.fixture
def logged_driver(driver):
    """Driver que ya entra logueado para probar el inventario."""
    from pages.login_page import LoginPage

    LoginPage(driver).open(BASE_URL).login(USERNAME, PASSWORD)
    return driver


@pytest.fixture(scope="session")
def credentials():
    return {"username": USERNAME, "password": PASSWORD}


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


def pytest_configure(config):
    Path("reports").mkdir(exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda una captura y la URL si una prueba falla."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver") or item.funcargs.get("logged_driver")
    if browser is None:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = item.name.replace("/", "_")
    screenshot = EVIDENCE_DIR / f"{safe_name}_{timestamp}.png"
    browser.save_screenshot(str(screenshot))
    (EVIDENCE_DIR / f"{safe_name}_{timestamp}.txt").write_text(
        f"URL: {browser.current_url}\nTítulo: {browser.title}\n",
        encoding="utf-8",
    )
    logger.error("La prueba %s falló. Evidencia: %s", item.name, screenshot)
