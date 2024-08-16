from typing import List
import model
import db
import re
from datetime import datetime

TITLE_LIMIT = 30
TEXT_LIMIT = 200

class LogicException(Exception):
    pass


# Класс логики работы с событиями
class EventLogic:
    def __init__(self):
        self._event_db = db.EventDB()


    # Функция проверки валидности даты события
    def _validate_date(self, date: str):
        # Проверяем формат даты
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            raise LogicException('Date format is incorrect, should be YYYY-MM-DD')
        # Проверяем корректность даты
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise LogicException('Invalid date: the month or day is out of range')


    # Функция проверки валидности события
    def _validate_event(self, event: model.Event, is_update: bool = False, event_id: str = None):
        if event is None:
            raise LogicException('event is None')

        self._validate_date(event.date)
        
		# Проверяем длину заголовка и текста
        if event.title is None or len(event.title) > TITLE_LIMIT:
            raise LogicException(f'title length > MAX: {TITLE_LIMIT}')
        if event.text is None or len(event.text) > TEXT_LIMIT:
            raise LogicException(f'text length > MAX: {TEXT_LIMIT}')

        existing_events = self.list()

        # Проверяем наличие события с таким же датой в БД, если это не редактирование
        for existing_event in existing_events:
            if existing_event.date == event.date:
                if is_update:
                    if existing_event.id != event_id:
                        raise LogicException(f'An event already exists for the date: {event.date}')
                else:
                    raise LogicException(f'An event already exists for the date: {event.date}')


    # Проверка нового события
    def create(self, event: model.Event) -> str:
        self._validate_event(event, is_update=False)
        try:
            return self._event_db.create(event)
        except Exception as ex:
            raise LogicException(f'failed CREATE operation with: {ex}')


    # Проверка вывода списка всех событий
    def list(self) -> List[model.Event]:
        try:
            return self._event_db.list()
        except Exception as ex:
            raise LogicException(f'failed LIST operation with: {ex}')


    # Проверка чтения конкретного события
    def read(self, _id: str) -> model.Event:
        try:
            return self._event_db.read(_id)
        except Exception as ex:
            raise LogicException(f'failed READ operation with: {ex}')


    # Проверка изменения события
    def update(self, _id: str, event: model.Event):
        self._validate_event(event, is_update=True, event_id=_id)
        try:
            return self._event_db.update(_id, event)
        except Exception as ex:
            raise LogicException(f'failed UPDATE operation with: {ex}')


    # Проверка удаления события
    def delete(self, _id: str):
        try:
            return self._event_db.delete(_id)
        except Exception as ex:
            raise LogicException(f'failed DELETE operation with: {ex}')
