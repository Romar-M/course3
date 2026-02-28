# src/aeroplane.py
"""
Модуль с классом Aeroplane, представляющим информацию о самолёте.
"""

from typing import Union, Any


class Aeroplane:
    """
    Класс, представляющий информацию о самолёте.

    Атрибуты:
        callsign (str): позывной рейса
        origin_country (str): страна регистрации
        velocity (float): скорость (м/с)
        altitude (float): высота (м)
        on_ground (bool): находится ли на земле
    """
    __slots__ = ('_callsign', '_origin_country', '_velocity', '_altitude', '_on_ground')

    def __init__(self, callsign: str, origin_country: str, velocity: float, altitude: float, on_ground: bool):
        """
        Инициализирует экземпляр Aeroplane с валидацией данных.
        """
        self._callsign = self._validate_string(callsign, 'callsign')
        self._origin_country = self._validate_string(origin_country, 'origin_country')
        self._velocity = self._validate_float(velocity, 'velocity')
        self._altitude = self._validate_float(altitude, 'altitude')
        self._on_ground = self._validate_bool(on_ground, 'on_ground')

    # ---------- Приватные методы валидации ----------
    @staticmethod
    def _validate_string(value: Any, name: str) -> str:
        """Проверяет, что значение является непустой строкой."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _validate_float(value: Any, name: str) -> float:
        """Проверяет, что значение является неотрицательным числом."""
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{name} must be a number")
        if val < 0:
            raise ValueError(f"{name} cannot be negative")
        return val

    @staticmethod
    def _validate_bool(value: Any, name: str) -> bool:
        """Проверяет, что значение является булевым."""
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a boolean")
        return value

    # ---------- Свойства для доступа к атрибутам (инкапсуляция) ----------
    @property
    def callsign(self) -> str:
        """Возвращает позывной."""
        return self._callsign

    @property
    def origin_country(self) -> str:
        """Возвращает страну регистрации."""
        return self._origin_country

    @property
    def velocity(self) -> float:
        """Возвращает скорость (м/с)."""
        return self._velocity

    @property
    def altitude(self) -> float:
        """Возвращает высоту (м)."""
        return self._altitude

    @property
    def on_ground(self) -> bool:
        """Возвращает флаг нахождения на земле."""
        return self._on_ground

    # ---------- Магические методы для сравнения по высоте ----------
    def __eq__(self, other: object) -> bool:
        """Сравнение на равенство высот."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude == other.altitude

    def __lt__(self, other: object) -> bool:
        """Меньше (по высоте)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude < other.altitude

    def __le__(self, other: object) -> bool:
        """Меньше или равно (по высоте)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude <= other.altitude

    # Дополнительный метод для сравнения по скорости (не является магическим,
    # но позволяет сравнивать по скорости отдельно).
    def compare_speed(self, other: 'Aeroplane') -> int:
        """
        Сравнивает самолёты по скорости.

        Args:
            other: другой экземпляр Aeroplane

        Returns:
            -1 если скорость текущего меньше, 0 если равны, 1 если больше.
        """
        if not isinstance(other, Aeroplane):
            raise TypeError("Can only compare with another Aeroplane")
        if self.velocity < other.velocity:
            return -1
        elif self.velocity > other.velocity:
            return 1
        return 0

    # ---------- Сериализация ----------
    def to_dict(self) -> dict:
        """Возвращает словарь с данными самолёта."""
        return {
            'callsign': self.callsign,
            'origin_country': self.origin_country,
            'velocity': self.velocity,
            'altitude': self.altitude,
            'on_ground': self.on_ground
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Aeroplane':
        """
        Создаёт объект Aeroplane из словаря.

        Args:
            data: словарь с ключами, соответствующими атрибутам

        Returns:
            Новый экземпляр Aeroplane
        """
        return cls(
            callsign=data['callsign'],
            origin_country=data['origin_country'],
            velocity=data['velocity'],
            altitude=data['altitude'],
            on_ground=data['on_ground']
        )

    def __repr__(self) -> str:
        """Представление объекта для отладки."""
        return (f"Aeroplane(callsign={self.callsign!r}, "
                f"origin_country={self.origin_country!r}, "
                f"velocity={self.velocity:.1f}, altitude={self.altitude:.1f}, "
                f"on_ground={self.on_ground})")
