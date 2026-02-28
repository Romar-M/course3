# src/api.py
"""
Модуль для работы с внешними API: Nominatim (OpenStreetMap) и OpenSky.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any, Tuple
import requests


class BaseAPI(ABC):
    """
    Абстрактный базовый класс для работы с внешними API.
    Определяет интерфейс для подключения и получения данных о самолётах.
    """

    @abstractmethod
    def _connect(self, url: str, params: Optional[Dict] = None,
                 headers: Optional[Dict] = None) -> Optional[Any]:
        """
        Выполняет GET-запрос к указанному URL и возвращает JSON-ответ.

        Args:
            url: адрес запроса
            params: параметры запроса (query string)
            headers: заголовки HTTP

        Returns:
            JSON-ответ в виде объекта Python (обычно dict или list) или None при ошибке.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Получает список самолётов, находящихся в воздушном пространстве указанной страны.

        Args:
            country: название страны (например, "Canada")

        Returns:
            Список словарей, каждый словарь содержит данные об одном самолёте.
            Если данные получить не удалось, возвращается пустой список.
        """
        pass


class AeroplanesAPI(BaseAPI):
    """
    Реализация API для получения данных о самолётах через сервисы Nominatim и OpenSky.
    """

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Инициализирует клиента для работы с API.

        Args:
            username: имя пользователя OpenSky (опционально, для повышенных лимитов)
            password: пароль OpenSky (опционально)
        """
        self._openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self._opensky_url = 'https://opensky-network.org/api/states/all'
        self._session = requests.Session()
        if username and password:
            self._session.auth = (username, password)
        # Заголовок User-Agent обязателен для Nominatim
        self._headers_nominatim = {'User-Agent': 'aeroplane-project/1.0'}

    def _connect(self, url: str, params: Optional[Dict] = None,
                 headers: Optional[Dict] = None) -> Optional[Any]:
        """
        Приватный метод для выполнения GET-запроса с обработкой ошибок.
        """
        try:
            response = self._session.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                # В реальном проекте здесь можно логировать ошибку
                return None
        except requests.RequestException:
            return None

    def _get_boundingbox(self, country: str) -> Optional[Tuple[float, float, float, float]]:
        """
        Получает boundingbox страны через Nominatim API.

        Args:
            country: название страны

        Returns:
            Кортеж (min_latitude, max_latitude, min_longitude, max_longitude)
            или None, если страна не найдена.
        """
        params = {
            'country': country,
            'format': 'json',
            'limit': 1
        }
        data = self._connect(self._openstreetmap_url, params, self._headers_nominatim)
        if not data or len(data) == 0:
            return None

        boundingbox = data[0].get('boundingbox')
        if not boundingbox or len(boundingbox) < 4:
            return None

        # Преобразуем строки в числа с плавающей точкой
        try:
            bbox = tuple(float(x) for x in boundingbox[:4])
            # Порядок: [min_lat, max_lat, min_lon, max_lon]
            return bbox  # (south, north, west, east)
        except ValueError:
            return None

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Получает список самолётов для указанной страны.
        """
        # 1. Получаем boundingbox страны
        bbox = self._get_boundingbox(country)
        if bbox is None:
            return []

        # 2. Запрашиваем самолёты в этом прямоугольнике через OpenSky
        lamin, lamax, lomin, lomax = bbox
        params = {
            'lamin': lamin,
            'lamax': lamax,
            'lomin': lomin,
            'lomax': lomax
        }
        opensky_data = self._connect(self._opensky_url, params)
        if not opensky_data or 'states' not in opensky_data:
            return []

        # 3. Преобразуем ответ в список словарей с понятными ключами
        states = opensky_data['states']
        # Поля согласно документации OpenSky (индексы)
        keys = [
            'icao24', 'callsign', 'origin_country', 'time_position',
            'last_contact', 'longitude', 'latitude', 'baro_altitude',
            'on_ground', 'velocity', 'true_track', 'vertical_rate',
            'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source'
        ]

        result = []
        for state in states:
            if state is None:
                continue
            # Создаём словарь, пропуская null-значения (они останутся None)
            row = dict(zip(keys, state))
            result.append(row)

        return result
