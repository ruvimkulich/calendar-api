from typing import List
import model


class StorageException(Exception):
    pass

# Класс для работы с локальным хранилищем
class LocalStorage:
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    # Создание нового события
    def create(self, event: model.Event) -> str: 
        self._id_counter += 1
        event.id = str(self._id_counter)
        self._storage[event.id] = event
        return event.id

    # Возвращает список всех событий
    def list(self) -> List[model.Event]:  
        return list(self._storage.values())

    # Возвращает событие по его идентификатору
    def read(self, _id: str) -> model.Event: 
        if _id not in self._storage:
            raise StorageException(f'{_id} not found in storage')
        return self._storage[_id]

    # Обновляет событие по его идентификатору
    def update(self, _id: str, event: model.Event):
        if _id not in self._storage:
            raise StorageException(f'{_id} not found in storage')
        event.id = _id
        self._storage[event.id] = event

    # Удаляет событие по его идентификатору
    def delete(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f'{_id} not found in storage')
        del self._storage[_id]
