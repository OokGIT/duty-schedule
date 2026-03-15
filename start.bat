@echo off
echo ========================================
echo   Система управління графіком чергувань
echo   Django + MariaDB
echo ========================================
echo.
echo Запуск додатку...
echo.

python manage.py runserver

if errorlevel 1 (
    echo.
    echo Помилка: Python не знайдено або проблема з налаштуваннями!
    echo.
    echo Будь ласка, переконайтеся, що:
    echo 1. Встановлено Python з https://www.python.org/downloads/
    echo 2. Встановлено MariaDB/MySQL
    echo 3. Створено базу даних 'duty_schedule'
    echo 4. Налаштовано файл .env
    echo.
    pause
)
