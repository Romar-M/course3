# src/storage.py
"""
Модуль для работы с хранилищем данных о самолётах.
Содержит абстрактный базовый класс BaseStorage и реализацию для JSON-файлов.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import os


class BaseStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем данных о самолётах.
    Определяет интерфейс для добавления, получения и удаления записей.
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: 'Aeroplane') -> None:
        """
        Добавляет информацию о самолёте в хранилище.
        Реализация должна избегать дублирования данных (например, по callsign).
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria) -> List[Dict[str, Any]]:
        """
        Возвращает список самолётов, соответствующих указанным критериям.
        Критерии передаются как именованные аргументы, например:
            get_aeroplanes(origin_country='Russia', on_ground=True)
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, **criteria) -> None:
        """
        Удаляет все записи о самолётах, соответствующих критериям.
        """
        pass


class JSONSaver(BaseStorage):
    """
    Реализация хранилища в JSON-файле.
    Каждая запись — словарь с данными самолёта.
    Файл создаётся автоматически при первом обращении.
    """

    def __init__(self, filename: str = 'aeroplanes.json'):
        """
        Инициализирует хранилище с указанным именем файла.

        Args:
            filename: имя JSON-файла (по умолчанию 'aeroplanes.json')
        """
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создаёт пустой JSON-файл со списком, если его нет."""
        if not os.path.exists(self._filename):
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_data(self) -> List[Dict]:
        """Загружает все данные из файла."""
        with open(self._filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data: List[Dict]) -> None:
        """Сохраняет данные в файл."""
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_aeroplane(self, aeroplane: 'Aeroplane') -> None:
        """
        Добавляет самолёт в файл, если такой позывной ещё не существует.
        Для проверки уникальности используется поле 'callsign'.
        """
        data = self._load_data()
        # Проверяем, есть ли уже самолёт с таким позывным
        callsign = aeroplane.callsign
        if not any(item.get('callsign') == callsign for item in data):
            data.append(aeroplane.to_dict())
            self._save_data(data)

    def get_aeroplanes(self, **criteria) -> List[Dict[str, Any]]:
        """
        Возвращает список самолётов, удовлетворяющих критериям.
        Если критерии не заданы, возвращает все записи.
        """
        data = self._load_data()
        if not criteria:
            return data

        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def delete_aeroplane(self, **criteria) -> None:
        """
        Удаляет все записи, соответствующие критериям.
        Если критерии не заданы, ничего не удаляет (чтобы случайно не стереть всё).
        """
        if not criteria:
            return  # Не удаляем всё без явного запроса

        data = self._load_data()
        new_data = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if not match:
                new_data.append(item)
        self._save_data(new_data)


# -------------------------------------------------------------------
# Дополнительные классы для других форматов (по желанию)
# -------------------------------------------------------------------

class CSVSaver(BaseStorage):
    """
    Заглушка для сохранения в CSV-файл.
    В реальном проекте здесь была бы реализация с использованием модуля csv.
    """
    def __init__(self, filename: str = 'aeroplanes.csv'):
        self._filename = filename
        # TODO: реализовать

    def add_aeroplane(self, aeroplane: 'Aeroplane') -> None:
        pass

    def get_aeroplanes(self, **criteria) -> List[Dict[str, Any]]:
        return []

    def delete_aeroplane(self, **criteria) -> None:
        pass


class TXTSaver(BaseStorage):
    """
    Заглушка для сохранения в текстовый файл.
    """
    def __init__(self, filename: str = 'aeroplanes.txt'):
        self._filename = filename
        # TODO: реализовать

    def add_aeroplane(self, aeroplane: 'Aeroplane') -> None:
        pass

    def get_aeroplanes(self, **criteria) -> List[Dict[str, Any]]:
        return []

    def delete_aeroplane(self, **criteria) -> None:
        pass
