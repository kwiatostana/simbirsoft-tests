from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class FormPage(BasePage):
    """Страница с формой для заполнения, реализует Page Object Model + Page Factory + Fluent паттерны"""
    
    URL = "https://practice-automation.com/form-fields/"
    
    # Локаторы элементов (используем CSS, XPath и ID)
    # CSS селекторы
    NAME_FIELD = (By.CSS_SELECTOR, "#name-input")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[id*='email']")
    
    # XPath локаторы для напитков (Milk и Coffee)
    DRINK_MILK = (By.XPATH, "//input[@value='Milk' or @value='milk']")
    DRINK_COFFEE = (By.XPATH, "//input[@value='Coffee' or @value='coffee']")
    
    # XPath для цвета (Yellow)
    COLOR_YELLOW = (By.XPATH, "//input[@value='Yellow' or @value='yellow']")
    
    # ID локаторы
    AUTOMATION_SELECT = (By.ID, "automation")
    MESSAGE_AREA = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    
    # Локаторы для анализа Automation tools (согласно ТЗ)
    AUTOMATION_TOOLS_LIST = (By.XPATH, "//*[contains(text(),'Automation tools') or contains(text(),'automation tools')]//following::ul[1]//li | //*[contains(text(),'Automation tools') or contains(text(),'automation tools')]//parent::*//ul//li")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Открыть страницу с формой")
    def open_form_page(self):
        """Открывает страницу с формой (Fluent interface)"""
        return self.open(self.URL)
    
    @allure.step("Заполнить имя: '{name}'")
    def fill_name(self, name):
        """Заполняет поле имени (Fluent interface)"""
        return self.type(self.NAME_FIELD, name)
    
    @allure.step("Заполнить пароль")
    def fill_password(self, password):
        """Заполняет поле пароля (Fluent interface)"""
        return self.type(self.PASSWORD_FIELD, password)
    
    @allure.step("Заполнить email: '{email}'")
    def fill_email(self, email):
        """Заполняет поле email (Fluent interface)"""
        return self.type(self.EMAIL_FIELD, email)
    
    @allure.step("Выбрать напитки: Milk и Coffee")
    def select_favorite_drinks(self):
        """Выбирает Milk и Coffee (Fluent interface)"""
        self.click(self.DRINK_MILK)
        self.click(self.DRINK_COFFEE)
        return self
    
    @allure.step("Выбрать цвет: Yellow")
    def select_yellow_color(self):
        """Выбирает цвет Yellow (Fluent interface)"""
        return self.click(self.COLOR_YELLOW)
    
    @allure.step("Выбрать автоматизацию: '{value}'")
    def select_automation(self, value):
        """Выбирает значение в select automation (Fluent interface)"""
        return self.select_by_value(self.AUTOMATION_SELECT, value)
    
    @allure.step("Заполнить сообщение: '{message}'")
    def fill_message(self, message):
        """Заполняет текстовое поле сообщения (Fluent interface)"""
        return self.type(self.MESSAGE_AREA, message)
    
    @allure.step("Нажать кнопку Submit")
    def click_submit(self):
        """Нажимает кнопку отправки формы (Fluent interface)"""
        return self.click(self.SUBMIT_BUTTON)
    
    @allure.step("Подсчитать инструменты в разделе Automation tools")
    def count_automation_tools(self):
        """Подсчитывает количество инструментов в разделе Automation tools согласно ТЗ"""
        tools = self.find_elements(self.AUTOMATION_TOOLS_LIST)
        count = len(tools)
        allure.attach(
            f"Найдено инструментов в Automation tools: {count}",
            name="Количество Automation tools",
            attachment_type=allure.attachment_type.TEXT
        )
        return count
    
    @allure.step("Найти самый длинный инструмент в Automation tools")
    def find_longest_automation_tool(self):
        """Находит инструмент с наибольшим количеством символов в Automation tools согласно ТЗ"""
        tools = self.find_elements(self.AUTOMATION_TOOLS_LIST)
        
        if not tools:
            return ""
        
        tool_texts = [tool.text.strip() for tool in tools if tool.text.strip()]
        
        if not tool_texts:
            return ""
        
        longest_tool = max(tool_texts, key=len)
        allure.attach(
            f"Самый длинный инструмент: '{longest_tool}' (длина: {len(longest_tool)})",
            name="Анализ Automation tools",
            attachment_type=allure.attachment_type.TEXT
        )
        return longest_tool
    
    @allure.step("Заполнить всю форму согласно требованиям")
    def fill_complete_form_according_to_tz(self, name, password, email, automation_choice="yes"):
        """
        Заполняет всю форму с использованием Fluent interface
        Создаёт сообщение на основе анализа Automation tools
        """
        tools_count = self.count_automation_tools()
        longest_tool = self.find_longest_automation_tool()
        message = f"Количество инструментов в Automation tools: {tools_count}. Самый длинный инструмент: {longest_tool}"
        
        # Заполняем форму (Fluent interface)
        return (self.fill_name(name)
                .fill_password(password)
                .select_favorite_drinks()
                .select_yellow_color()
                .select_automation(automation_choice)
                .fill_email(email)
                .fill_message(message))
    
    @allure.step("Отправить форму и проверить результат")
    def submit_and_verify(self, expected_alert_text="Message received!"):
        """Отправляет форму и проверяет появление алерта с ожидаемым текстом"""
        self.click_submit()
        alert_text = self.accept_alert()
        
        if alert_text:
            allure.attach(
                f"Текст алерта: '{alert_text}'",
                name="Результат отправки",
                attachment_type=allure.attachment_type.TEXT
            )
            return alert_text == expected_alert_text
        return False