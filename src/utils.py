# src/utils.py
"""
Вспомогательные функции для работы со списками самолётов:
фильтрация, сортировка, вывод.
"""

from typing import List, Optional
from .aeroplane import Aeroplane


def filter_by_origin_country(aeroplanes: List[Aeroplane], countries: List[str]) -> List[Aeroplane]:
    """
    Оставляет только самолёты, страна регистрации которых входит в список countries.

    Args:
        aeroplanes: исходный список самолётов
        countries: список стран для фильтрации (если пуст, возвращается исходный список)

    Returns:
        Отфильтрованный список
    """
    if not countries:
        return aeroplanes
    countries_set = set(countries)
    return [a for a in aeroplanes if a.origin_country in countries_set]


def filter_by_altitude_range(aeroplanes: List[Aeroplane],
                              min_alt: Optional[float],
                              max_alt: Optional[float]) -> List[Aeroplane]:
    """
    Оставляет самолёты, высота которых находится в заданном диапазоне [min_alt, max_alt].
    Границы включаются. Если какая-либо граница не указана (None), она игнорируется.

    Args:
        aeroplanes: исходный список
        min_alt: минимальная высота (включительно) или None
        max_alt: максимальная высота (включительно) или None

    Returns:
        Отфильтрованный список
    """
    result = aeroplanes
    if min_alt is not None:
        result = [a for a in result if a.altitude >= min_alt]
    if max_alt is not None:
        result = [a for a in result if a.altitude <= max_alt]
    return result


def filter_by_on_ground(aeroplanes: List[Aeroplane], on_ground: bool) -> List[Aeroplane]:
    """
    Оставляет самолёты, соответствующие состоянию на земле/в воздухе.

    Args:
        aeroplanes: исходный список
        on_ground: True – только на земле, False – только в воздухе

    Returns:
        Отфильтрованный список
    """
    return [a for a in aeroplanes if a.on_ground == on_ground]


def sort_by_altitude(aeroplanes: List[Aeroplane], reverse: bool = True) -> List[Aeroplane]:
    """
    Сортирует список самолётов по высоте.

    Args:
        aeroplanes: исходный список
        reverse: если True – по убыванию (сначала самые высокие), иначе по возрастанию

    Returns:
        Новый отсортированный список
    """
    return sorted(aeroplanes, reverse=reverse)


def get_top_n(aeroplanes: List[Aeroplane], n: int) -> List[Aeroplane]:
    """
    Возвращает первые n элементов списка (предполагается, что список уже отсортирован).

    Args:
        aeroplanes: исходный список
        n: количество элементов

    Returns:
        Список из первых n элементов (или меньше, если исходный список короче)
    """
    return aeroplanes[:n]


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """
    Красиво выводит информацию о самолётах в консоль.

    Args:
        aeroplanes: список самолётов
    """
    if not aeroplanes:
        print("Нет данных для отображения.")
        return

    print(f"\n{'№':<4} {'Позывной':<12} {'Страна регистрации':<20} {'Скорость (м/с)':<15} {'Высота (м)':<12} {'На земле':<10}")
    print('-' * 80)
    for i, a in enumerate(aeroplanes, start=1):
        on_ground_str = 'Да' if a.on_ground else 'Нет'
        print(f"{i:<4} {a.callsign:<12} {a.origin_country:<20} {a.velocity:<15.1f} {a.altitude:<12.1f} {on_ground_str:<10}")
    print()
