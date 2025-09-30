from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    """Базовый класс для всех страниц, реализует основные методы работы с элементами"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    @allure.step("Открыть URL: {url}")
    def open(self, url):
        """Открывает указанный URL"""
        self.driver.get(url)
        return self
    
    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator, timeout=10):
        """Находит элемент по локатору с ожиданием"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"Element not found: {locator}",
                attachment_type=allure.attachment_type.PNG
            )
            raise
    
    @allure.step("Найти элементы: {locator}")
    def find_elements(self, locator, timeout=10):
        """Находит элементы по локатору с ожиданием"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator, timeout=10):
        """Кликает по элементу с ожиданием его реагирования"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            # Сначала пробуем скроллить к элементу
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            element.click()
        except Exception:
            # Если обычный клик не работает используем JavaScript
            self.driver.execute_script("arguments[0].click();", element)
        return self
    
    @allure.step("Ввести текст '{text}' в поле: {locator}")
    def type(self, locator, text, timeout=10):
        """Вводит текст в поле с предварительной очисткой"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return self
    
    @allure.step("Выбрать значение '{value}' в селекте: {locator}")
    def select_by_value(self, locator, value, timeout=10):
        """Выбирает значение в select по value"""
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
        return self
    
    @allure.step("Выбрать текст '{text}' в селекте: {locator}")
    def select_by_visible_text(self, locator, text, timeout=10):
        """Выбирает значение в select по видимому тексту"""
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
        return self
    
    @allure.step("Ждать появления алерта")
    def wait_for_alert(self, timeout=10):
        """Ожидает появления JavaScript alert"""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
    
    @allure.step("Принять алерт")
    def accept_alert(self):
        """Принимает JavaScript alert"""
        alert = self.wait_for_alert()
        if alert:
            alert_text = alert.text
            alert.accept()
            return alert_text
        return None
    
    @allure.step("Сделать скриншот")
    def take_screenshot(self, name="screenshot"):
        """Делает скриншот и прикрепляет к отчету"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
