## Разработанный на Django REST-сервис друзей.

[Документация](./Documentation/documentation.md) - описание и примеры взаимодействия с сервисом.

Исходный код проекта лежит в папке [FriendsService](./FriendsService).

[Dockerfile](./FriendsService/Dockerfile) - образ сервиса. Собирает контейнер, подтягивает Django код с текущего репозитория github. Требуемые зависимости
python уже сформированы в лежащем здесь же [requirements.txt](./FriendsService/requirements.txt).

Дополнительно были написаны [unit-тесты](./FriendsService/main/tests.py) для приложения. Их описание добавлено в документацию.
