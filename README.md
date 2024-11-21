# Wish Craft

**WishCraft** — это платформа для публикации и реализации желаний за деньги. Пользователи могут создавать свои желания, устанавливать стоимость их выполнения и делиться ими с другими участниками платформы.


## Содержание
- [Описание](#описание)
- [Запуск проекта](#запуск-проекта)
  - [Без Docker](#без-docker)
  - [С Docker](#c-docker)

## Описание
Описания нет

## Запуск проекта

### Без Docker

#### Требования
- Python 3.8 +
- PostgreSQL
- Redis

#### Инструкции
   
##### Установка зависимостей:

    pip install -r requirements.txt

##### Создайте файл .env и настройте переменные окружения (Пример переменных в файле 'env_template') 
   
    Пример переменных окружения в файле 'env_tamplate'

##### Применение :

    python manage.py migrate

##### Соберите статические файлы:
   
    python manage.py collectstatic

##### Создайте суперюзера:
   
    python manage.py createsuperuser
   
##### Запустите проект и celery:

    python manage.py runserver
    celery -A core worker -l INFO

### C Docker
#### Требования
- Python 3.8 +
- Docker (Docker-compose)


#### Инструкции
##### Клонируйте репозиторий:
 
    git clone https://github.com/AnvarS21/wishcraft.git
   
##### Создайте файл .env и настройте переменные окружения 
    
    Пример переменных окружения в файле 'env_tamplate'

##### Запустите Docker-compose
   
    docker-compose up --build -d

##### Зайдите в bash backend:

    docker-compose exec backend bash

##### Соберите статические файлы и создайте суперюзера:
   
    python manage.py collectstatic
    python manage.py createsuperuser


