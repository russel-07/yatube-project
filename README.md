# Yatube
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

Yatube - это сервис для публикации личных дневников. Здесь можно создать свою страницу, просматривать страницы других авторов, подписываться на авторов и комментировать их записи.
Записи можно добавлять в тематические сообщества и просматривать там записи разных авторов.

## Функциональность проекта
- Регистрация новых пользователей;
- Система восстановления пароля;
- Создание/редактирование/удаление новых записей;
- Создание комментариев к записям;
- Подписка на других авторов;
- Пагинация;
- Кэширование;
- Админ-зона.

## Запуск и развертывание приложения
- Cклонируйте данный репозиторий:
    ```bash
    git clone https://github.com/russel-07/yatube-project.git
    ```

- Откройте проект, создайте и запустите виртуальное окружение:
    ```bash
    python -m venv venv && source venv/Scripts/activate
    ```

- Установите пакеты виртуального окружения:
    ```bash
    pip install -r requirements.txt
    ```

- Выполните миграции:
    ```bash
    python manage.py migrate
    ```

- Выполните команду сбора статики:
    ```bash
    python manage.py collectstatic --no-input
    ```

- При необходимости заполните базу данных тестовыми данными из файла 'fixtures.json':
    ```bash
    python manage.py loaddata fixtures.json
    ```

- Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

- Запустите проект:
    ```bash
    python manage.py runserver
    ```

- В браузере по адресу [localhost:8000](http://localhost:8000/) будет доступно приложение Yatube. Приложение будет запущено в режиме отладки с эмуляцией почтового сервера, все письма будут создаваться в директории `sent_emails`;
 
- На страницу администрирования можно войти по данным суперпользователя по адресу [localhost:8000/admin/](http://localhost:8000/admin/).