from typing import List
import model
import storage


class DBException(Exception):
    pass


# Класс для работы с базой данных событий
class EventDB:
    def __init__(self):
        self._storage = storage.LocalStorage()

    # Создание нового события
    def create(self, event: model.Event) -> str:
        try:
            return self._storage.create(event)
        except Exception as ex:
            raise DBException(f'failed CREATE operation with: {ex}')

    # Получение списка всех событий

    def list(self) -> List[model.Event]:
        try:
            return self._storage.list()
        except Exception as ex:
            raise DBException(f'failed LIST operation with: {ex}')

    # Получение конкретного события по идентификатору

    def read(self, _id: str) -> model.Event:
        try:
            return self._storage.read(_id)
        except Exception as ex:
            raise DBException(f'failed READ operation with: {ex}')

    # Обновление события по идентификатору

    def update(self, _id: str, event: model.Event):
        try:
            return self._storage.update(_id, event)
        except Exception as ex:
            raise DBException(f'failed UPDATE operation with: {ex}')

    # Удаление события по идентификатору

    def delete(self, _id: str):
        try:
            return self._storage.delete(_id)
        except Exception as ex:
            raise DBException(f'failed DELETE operation with: {ex}')
