# Сервис для работы с Календарем
### Техническая информация


API интерфейс CRUD (Добавление / Список / Чтение / Обновление / Удаление).

Модель данных "Событие": ID, Дата, Заголовок, Текст.  
Формат данных: "ГГГГ-ММ-ДД|заголовок|текст".  
Максимальная длина заголовка — 30 символов.  
Максимальная длина поля Текст — 200 символов.

События сохраняются в локальном хранилище данных.  
Нельзя добавить больше одного события в день!

<br/>

## Запуск приложения

В командной строке Windows перейти в каталог с программой и ввести поочередно  следующие команды:
1. `.venv\Scripts\activate.bat` - запуск виртуального окружения Python;
2. `python -m pip install -r requirements.txt` - установка зависимостей; 
3. `flask --app calendar\server.py run` - запуск сервера разработки.

<br/>

## cURL тестирование

#### Добавление новой заметки / дата == 2000-12-31
```
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2000-12-31|title|text"
```

#### Получение всего списка заметок
```
curl http://127.0.0.1:5000/api/v1/calendar/
```

#### Получение заметки по идентификатору / ID == 1
```
curl http://127.0.0.1:5000/api/v1/calendar/1/
```

#### Обновление текста заметки по идентификатору / ID == 1 /  новый текст == "new text"
```
curl http://127.0.0.1:5000/api/v1/calendar/1/ -X PUT -d "YYYY-MM-DD|title|new text"
```

#### Удаление заметки по идентификатору / ID == 1
```
curl http://127.0.0.1:5000/api/v1/calendar/1/ -X DELETE
```

<br/>

## Примеры работы
### Пример исполнения команд с выводом
1. Создание события
```
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2000-12-31|title1|text1"
new id: 1
```

2. Вывод списка всех событий
```
curl http://127.0.0.1:5000/api/v1/calendar/
1|2000-12-31|title1|text1
```

3. Вывод одного события по ID
```
curl http://127.0.0.1:5000/api/v1/calendar/1/
1|2000-12-31|title1|text1
```

4. Редактирования события по ID
```
curl http://127.0.0.1:5000/api/v1/calendar/1/ -X PUT -d "2000-12-31|title1|new text"
updated
```

5. Удаления события по ID
```
curl http://127.0.0.1:5000/api/v1/calendar/1/ -X DELETE
deleted
```

6. Вывод списка всех события после удаления события
```
curl http://127.0.0.1:5000/api/v1/calendar/
-- пусто --
```
<br/>

### Пример исполнения команд с ошибками
- Добавление события на занятую дату
```
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2000-12-31|title2|text2"
failed to CREATE with: An event already exists for the date: 2000-12-31
```

- Добавление события с несуществующей датой
```
http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2000-15-40|title|text"
failed to CREATE with: Invalid date: the month or day is out of range
```

- Добавление события с неверным форматом даты
```
http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2000-15-40|title|text"
failed to CREATE with: Date format is incorrect, should be YYYY-MM-DD
```

- Добавление события c превышением максимальной длины текста
```
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2001-12-31|title|looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong text"
failed to UPDATE with: text length > MAX: 200
```

- Добавление события c превышением максимальной длины заголовка
```
ccurl http://127.0.0.1:5000/api/v1/calendar/1/ -X POST -d "2001-12-31|loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong title|text"
failed to UPDATE with: title length > MAX: 30
```