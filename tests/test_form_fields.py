import pytest
import allure
from pages.form_page import FormPage


@allure.epic("Тестирование веб-формы")
@allure.feature("Заполнение и отправка формы")
class TestFormFields:
    """Тестовый класс для проверки функциональности формы на странице practice-automation.com"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка для каждого теста"""
        self.form_page = FormPage(driver)
        self.form_page.open_form_page()
    
    @allure.story("Позитивный тест-кейс")
    @allure.title("Успешное заполнение и отправка формы с валидными данными")
    @allure.description("""
    
    Ожидаемый результат: появился алерт с текстом Message received!
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_successful_form_submission(self):
        """Позитивный тест: успешное заполнение и отправка формы"""
        
        test_data = {
            "name": "TestUser",
            "password": "SecurePass123!",
            "email": "testuser@example.com",
            "automation": "yes"
        }
        
        with allure.step("Заполнить форму согласно требованиям"):
            self.form_page.fill_complete_form_according_to_tz(
                name=test_data["name"],
                password=test_data["password"],
                email=test_data["email"],
                automation_choice=test_data["automation"]
            )
        
        with allure.step("Сделать скриншот заполненной формы"):
            self.form_page.take_screenshot("Заполненная форма")
        
        # Assert - проверка результата
        with allure.step("Отправить форму и проверить успешный результат"):
            success = self.form_page.submit_and_verify("Message received!")
            assert success, "Алерт с подтверждением не появился или содержит неправильный текст"
    
    @allure.story("Негативный тест-кейс")  
    @allure.title("Отправка неполной формы")
    @allure.description("""
    Негативный тест: проверка поведения при отправке формы с незаполненными обязательными полями
 """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_incomplete_form_submission(self):
        """Негативный тест: проверка обязательности полей
        
        Цель: убедиться, что система требует заполнения всех обязательных полей
        Ожидание: форма не должна отправляться без заполнения имени
        """
        
        # Act - пытаемся отправить форму без заполнения имени (оставляем поле пустым)
        with allure.step("Заполнить форму БЕЗ обязательного поля Name (используя логику Automation tools)"):
            tools_count = self.form_page.count_automation_tools()
            longest_tool = self.form_page.find_longest_automation_tool()
            message = f"Количество инструментов в Automation tools: {tools_count}. Самый длинный инструмент: {longest_tool}"

            self.form_page.fill_password("TestPassword123") \
                         .select_favorite_drinks() \
                         .select_yellow_color() \
                         .select_automation("yes") \
                         .fill_email("test@example.com") \
                         .fill_message(message)
        
        with allure.step("Сделать скриншот неполной формы"):
            self.form_page.take_screenshot("Форма без имени")
        
        with allure.step("Попытаться отправить неполную форму"):
            self.form_page.click_submit()
        
        # Assert - проверка валидации обязательных полей
        with allure.step("Проверить, что форма не отправилась без обязательного поля"):
            alert_text = self.form_page.accept_alert()
            
            # Негативный тест: форма НЕ должна показать успешный алерт без обязательного поля
            assert alert_text != "Message received!", \
                f"Ошибка: Форма отправилась без заполнения обязательного поля 'Name'. " \
                f"Ожидалась ошибка валидации, получен алерт: '{alert_text}'"
