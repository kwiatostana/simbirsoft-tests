import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import allure


@pytest.fixture(scope="function")
def driver():
    """Создаёт экземпляр WebDriver для каждого теста"""
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Автоматическая установка и настройка ChromeDriver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    
    # Закрываем браузер после теста
    try:
        driver.quit()
    except:
        pass


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(driver, request):
    """Автоматически прикрепляет скриншот при падении теста"""
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed and driver:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.fixture(autouse=True)
def attach_screenshot_on_success(driver, request):
    """Автоматически прикрепляет скриншот при успешном прохождении теста"""
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.passed and driver:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Success Screenshot",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для получения результата теста"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
