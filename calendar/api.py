from flask import Flask
from flask import request
import model
import logic

app = Flask(__name__)


_event_logic = logic.EventLogic()


class ApiException(Exception):
    pass

# Преобразование RAW-данных в модель Event


def _from_raw(raw_event: str) -> model.Event:
    parts = raw_event.split('|')
    if len(parts) == 3:
        event = model.Event()
        event.id = None
        event.date = parts[0]
        event.title = parts[1]
        event.text = parts[2]
        return event
    elif len(parts) == 4:
        event = model.Event()
        event.id = parts[0]
        event.date = parts[1]
        event.title = parts[2]
        event.text = parts[3]
        return event
    else:
        raise ApiException(f'invalid RAW event data {raw_event}')


# Преобразование модели Event в RAW-данные
def _to_raw(event: model.Event) -> str:
    if event.id is None:
        return f'{event.date}|{event.title}|{event.text}'
    else:
        return f'{event.id}|{event.date}|{event.title}|{event.text}'


API_ROOT = '/api/v1'
EVENT_API_ROOT = API_ROOT + '/calendar'


# Создание нового события
@app.route(EVENT_API_ROOT + '/', methods=['POST'])
def create():
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _id = _event_logic.create(event)
        return f'new id: {_id}', 201
    except Exception as ex:
        return f'failed to CREATE with: {ex}', 404


# Список всех событий
@app.route(EVENT_API_ROOT + '/', methods=['GET'])
def list():
    try:
        events = _event_logic.list()
        raw_event = ''
        for note in events:
            raw_event += _to_raw(note) + '\n'
        return raw_event, 200
    except Exception as ex:
        return f'failed to LIST with: {ex}', 404


# Чтение события по id
@app.route(EVENT_API_ROOT + '/<_id>/', methods=['GET'])
def read(_id: str):
    try:
        event = _event_logic.read(_id)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f'failed to READ with: {ex}', 404


# Редактирование события по id
@app.route(EVENT_API_ROOT + '/<_id>/', methods=['PUT'])
def update(_id: str):
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _event_logic.update(_id, event)
        return 'updated', 200
    except Exception as ex:
        return f'failed to UPDATE with: {ex}', 404


# Удаление события по id
@app.route(EVENT_API_ROOT + '/<_id>/', methods=['DELETE'])
def delete(_id: str):
    try:
        _event_logic.delete(_id)
        return 'deleted', 200
    except Exception as ex:
        return f'failed to DELETE with: {ex}', 404
