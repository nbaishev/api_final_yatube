# YaTube API
### Описание
*API для проекта YaTube*
### Технологии
Примененнные библиотеки указаны в файле requirements.txt
### Инструкции по запуску

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/nbaishev/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
## Автор
_nbaishev_