import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 1. Настройка браузера (Fixture)
@pytest.fixture
def driver():
    options = Options()
    # headless означает, что браузер запустится НЕВИДИМО (в фоне). 
    # Это нужно для GitHub, так как у серверов нет мониторов!
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    yield driver # Передаем браузер тесту
    driver.quit() # Закрываем после теста

# 2. Хук для автоскриншота при падении
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )