# OSIRISv2.1

# Установка и запуск
1. Устновите пакеты командой `pip install -r requirements.txt`
2. Заполните .env файл по шаблону
3. Настройте Базу Данных и примените миграции `python manage.py makemigrations` и `python manage.py migrate`
4. Запустите тестовый сервер `python manage.py runserver`
5. В другом окне терминала в виртуальном окружении запустите воркер celery `celery -A special worker -l info -P threads`
6. В другом окне терминала в виртуальном окружении запустите планировщик celery `celery -A special beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
