# UI Автотесты для Practice Automation

Проект содержит UI автотесты на Python для тестирования веб-формы на сайте [https://practice-automation.com/form-fields/](https://practice-automation.com/form-fields/).

## Пример Allure Отчета

Скриншоты из Allure отчета:

### Статистика
<img width="1217" height="569" alt="image" src="https://github.com/user-attachments/assets/db91ee08-01ea-4612-bd88-3dd94fc0c272" />
<img width="1201" height="562" alt="image" src="https://github.com/user-attachments/assets/1afbed91-c810-4150-8792-1b47cc570b64" />



### Детали позитивного тест-кейса
<img width="1230" height="372" alt="image" src="https://github.com/user-attachments/assets/2aa2a50e-6928-4d6e-ab0e-36e4cf49758c" />

### Детали негативного тест-кейса
<img width="1215" height="402" alt="image" src="https://github.com/user-attachments/assets/001bb070-d291-45a9-a561-9abcab9237ae" />


## Технический стек

- Python 3.10+
- Selenium WebDriver (Chrome)
- PyTest - фреймворк для тестирования
- Allure - генерация отчётов
- Page Object Model + Page Factory + Fluent паттерны

## Установка и запуск

### Предварительные требования

1. **Python 3.10+**
2. **Google Chrome браузер** установлен (любая актуальная версия)
3. **Git** для клонирования репозитория
4. **Интернет-соединение** для автоматической загрузки ChromeDriver

**Примечание**: ChromeDriver устанавливается автоматически при первом запуске тестов

### Установка зависимостей

```bash
# Клонируем репозиторий
git clone https://github.com/kwiatostana/simbirsoft-tests
cd simbirsoft-tests

# Устанавливаем зависимости
pip install -r requirements.txt
```

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск только позитивных тестов
pytest -m positive

# Запуск только негативных тестов  
pytest -m negative

# Запуск с подробным выводом
pytest -v
```

## Структура проекта

```
├── allure-2.35.1/          # Allure Commandline Tool
├── pages/                  # Page Object классы
│   ├── __init__.py
│   ├── base_page.py        # Базовый класс для всех страниц
│   └── form_page.py        # Класс страницы с формой
├── reports/                # HTML отчёты PyTest
├── allure-results/         # Результаты выполнения тестов для Allure
├── tests/                  # Тестовые сценарии
│   ├── __init__.py
│   └── test_form_fields.py # Основные тесты формы
├── conftest.py            # Конфигурация PyTest
├── pytest.ini            # Настройки PyTest
├── requirements.txt       # Зависимости Python
└── README.md             # Документация проекта
```

## Реализованные паттерны

### Page Object Model
- Все элементы и действия страницы инкапсулированы в классе `FormPage`
- Локаторы вынесены в константы класса
- Методы возвращают `self` для поддержки Fluent интерфейса

### Page Factory
- Использование Selenium WebDriverWait для ожидания элементов
- Автоматическое управление ожиданиями через базовый класс `BasePage`

### Fluent Interface
- Методы можно вызывать по цепочке: `page.fill_name().fill_email().submit()`
- Пример: `form_page.fill_complete_form().click_submit()`

### Типы локаторов
- CSS селекторы: `#name-input`, `input[type='password']`, `input[type='email']`
- XPath: `//input[@value='Milk']`, `//input[@value='Coffee']`, `//input[@value='Yellow']`
- ID: `automation`, `message`, `submit-btn`

## Описание тест-кейсов

### Позитивный тест-кейс

Название: `test_successful_form_submission`

Описание: Автоматизация формы

Предусловие:
1. Открыть браузер
2. Перейти по ссылке https://practice-automation.com/form-fields/

Шаги основные:
1. Заполнить поле Name
2. Заполнить поле Password
3. Из списка "What is your favorite drink?" выбрать Milk и Coffee
4. Из списка "What is your favorite color?" выбрать Yellow
5. В поле "Do you like automation?" выбрать любой вариант
6. Поле Email заполнить строкой формата name@example.com
7. В поле Message написать количество инструментов, описанных в пункте Automation tools, и написать инструмент из списка Automation tools, содержащий наибольшее количество символов
8. Нажать на кнопку Submit

Ожидаемый результат: появился алерт с текстом "Message received!"

### Негативный тест-кейс

Название: `test_incomplete_form_submission`

Описание: Проверка валидации обязательных полей при отправке формы

Шаги:
1. Заполнить поле Password
2. Из списка "What is your favorite drink?" выбрать Milk и Coffee
3. Из списка "What is your favorite color?" выбрать Yellow
4. В поле "Do you like automation?" выбрать любой вариант
5. Поле Email заполнить строкой формата name@example.com
6. В поле Message написать количество инструментов, описанных в пункте Automation tools, и написать инструмент из списка Automation tools, содержащий наибольшее количество символов
7. НЕ заполнять поле Name (оставить пустым)
8. Нажать на кнопку Submit

Ожидаемый результат: Форма НЕ должна отправляться без заполнения обязательного поля Name. Ожидается ошибка валидации, а не алерт "Message received!"

## Дополнительная функциональность

### Анализ Automation tools
Позитивный тест включает методы для анализа раздела Automation tools согласно требованиям:
- `count_automation_tools()` - подсчёт инструментов в разделе Automation tools
- `find_longest_automation_tool()` - поиск инструмента с наибольшим количеством символов
- Автоматическое формирование сообщения с результатами анализа

## Отчёты

Проект использует Allure для создания подробных отчётов о прохождении тестов. Чтобы сгенерировать и просмотреть отчёт, выполните следующие шаги:

**Запуск тестов и сбор результатов Allure:**
    Запустите тесты с помощью `pytest`. Результаты Allure будут автоматически сохранены в папке `allure-results` благодаря настройкам в `pytest.ini`.

    ```bash
    pytest -v
    ```

## Просмотр Allure отчета

Для просмотра Allure отчета локально, используйте следующую команду:

```bash
allure-2.35.1\bin\allure.bat serve allure-results
```

Эта команда запустит локальный веб-сервер и автоматически откроет отчет в вашем браузере. Закройте терминал, чтобы остановить сервер.

## Статус проекта

Проект полностью реализован и протестирован :)

## Контакты

Если есть вопросы по проекту - создайте Issue в GitHub репозитории

Данный проект создан как тестовое задание для SimbirSoft
