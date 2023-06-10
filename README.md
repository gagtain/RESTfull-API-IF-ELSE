# RESTfull API Drip-Chip
Данный проект реализован на основе  [Тех. Задания](https://docs.google.com/document/d/1cUVHZfEo4uMGJBBADbRMQzdTjSsySiFJ3xVvZ8DsQ7o) от компании SimbirSoft на конкурсе "IF-ELSE".\
____
## Описание
API состоит из 6 логических частей и 25 эндпойнтов, которые в общем составляют систему для отслеживания перемещений животных и изменения их состояния в зависимости от роли пользователя.
REST API сервис DRIP_CHIP был реализован на фреймворке Django и Django rest framework (DRF) для языка Python.
## Способ запуска
Перед началом работы необходимо настроить БД в файле Drip_Chip/Drip_Chip/settings.py в переменной DATABASES\
### установка зависимостей в папке Drip_Chip
~~~ 
python -m pip install -r requirements.txt  
~~~
### Запуск сервера
~~~
python manage.py runserver 
~~~
Теперь API доступно по url "localhost:8000"
## Альтенативный запуск через Docker
установить и разархивировать архив по [ссылке](https://disk.yandex.ru/d/ittJA-pFdWJnxA)\
в папке Source скачать image проекта
~~~
docker load -i animal_chipization_2022.tar
~~~
Запустить контейнер в папке Source
~~~
docker-compose up
~~~
В этом случае вместе с проектом запустятся тесты, доступные по url "localhost:8090", а сам проект будет доступен по url "localhost:8080"
## Результаты конкурса
Данный проект набрал 85 баллов из 100:
1. 70 из 70 за тесты
2. 5 из 15 за архитектуру
3. 10 из 15 за качество кода