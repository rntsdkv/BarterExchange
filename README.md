# Бартерный обмен

Сервис позволяет создавать объявления и обмениваться ими с другими пользователями на бартерной основе.

### Подготовка

1. Загрузить и распаковать zip-архив проекта
2. Открыть терминал и перейти в папку проекта
3. В терминале выполнить команду `pip install -r requirements.txt` или `pip3 install -r requirements.txt`
4. Выполнить миграцию, для этого в терминале выполнить команды
```
python manage.py makemigrations
python manage.py migrate
```
или
```
python3 manage.py makemigrations
python3 manage.py migrate
```
5. Для возможности использования, необходимо добавить категории объявлений, для этого нужно в терминале выполнить команды
`python manage.py dbshell` или `python3 manage.py dbshell`, затем выполнить команды
```
INSERT INTO ads_adcategory (title) VALUES ("Украшения");
INSERT INTO ads_adcategory (title) VALUES ("Продукты питания");
INSERT INTO ads_adcategory (title) VALUES ("Бытовые принадлежности");
INSERT INTO ads_adcategory (title) VALUES ("Мебель");
```

### Запуск сервера
В терминале выполнить команду `python manage.py runserver` или `python3 manage.py runserver`
После этого сайт будет доступен по адресу `127.0.0.1:8000`
Если нужно запустить на другом порту, нужно выполнить команду `python manage.py runserver 127.0.0.1:<порт>` или `python3 manage.py runserver 127.0.0.1:<порт>`

### Запуск тестов
В терминале выполнить команду `python manage.py test` или `python3 manage.py test`