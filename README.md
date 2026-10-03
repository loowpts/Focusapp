# Focusapp

Планировщик задач и трекер привычек на Django.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django_5.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

## Возможности

- **Задачи** (`main`): дедлайн, статус, приоритет, отметка о выполнении, календарь
  и JSON API для задач на выбранную дату.
- **Привычки** (`habit_tracker`): список привычек и ежедневные записи их выполнения.
- **Пользователи** (`users`): регистрация с подтверждением по email, профиль,
  вход/выход, сброс пароля по почте.

## Запуск

```bash
git clone https://github.com/loowpts/Focusapp.git
cd Focusapp
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # заполнить SECRET_KEY и доступ к PostgreSQL
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000, админка: http://127.0.0.1:8000/admin/.

С `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` письма подтверждения
и сброса пароля выводятся в консоль, SMTP не нужен.

## Структура

```
mysite/         настройки и корневые URL
main/           задачи, календарь, API
habit_tracker/  привычки и ежедневные записи
users/          регистрация, профиль, сброс пароля
```
