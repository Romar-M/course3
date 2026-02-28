# src/main.py
"""
Главный модуль программы.
Содержит функцию user_interaction, которая реализует интерфейс командной строки.
"""

from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.storage import JSONSaver
from src.utils import (
    filter_by_origin_country,
    filter_by_altitude_range,
    sort_by_altitude,
    get_top_n,
    print_aeroplanes
)


def user_interaction():
    """Основная функция взаимодействия с пользователем."""
    print("=" * 60)
    print("          ПОИСК САМОЛЁТОВ ПО СТРАНЕ")
    print("=" * 60)

    # 1. Ввод названия страны
    country = input("\nВведите название страны (например, Canada): ").strip()
    if not country:
        print("Страна не указана. Завершение работы.")
        return

    # 2. Ввод количества самолётов для топа
    top_n_input = input("Введите количество самолётов для вывода в топ N (по высоте): ").strip()
    try:
        top_n = int(top_n_input) if top_n_input else 5
    except ValueError:
        print("Некорректное число, будет использовано значение по умолчанию 5.")
        top_n = 5

    # 3. Ввод стран для фильтрации по регистрации (опционально)
    filter_countries_input = input("Введите страны для фильтрации по регистрации (через пробел, или оставьте пустым): ").strip()
    filter_countries = filter_countries_input.split() if filter_countries_input else []

    # 4. Ввод диапазона высот (опционально)
    altitude_range_input = input("Введите диапазон высот в формате 'min-max' (например, 5000-10000, или оставьте пустым): ").strip()
    min_alt, max_alt = None, None
    if altitude_range_input:
        parts = altitude_range_input.split('-')
        if len(parts) == 2:
            try:
                min_alt = float(parts[0]) if parts[0] else None
                max_alt = float(parts[1]) if parts[1] else None
            except ValueError:
                print("Некорректный диапазон высот, фильтр по высоте не применяется.")
        else:
            print("Некорректный формат, ожидается 'min-max'. Фильтр не применяется.")

    print(f"\nЗапрашиваю данные для страны '{country}'...")

    # 5. Получение данных через API
    api = AeroplanesAPI()  # без аутентификации (анонимно)
    raw_data = api.get_aeroplanes(country)

    if not raw_data:
        print("Не удалось получить данные о самолётах. Проверьте название страны или попробуйте позже.")
        return

    # 6. Преобразование сырых данных в список объектов Aeroplane
    aeroplanes = []
    for item in raw_data:
        try:
            # Из ответа OpenSky некоторые поля могут быть None; подставляем значения по умолчанию
            callsign = item.get('callsign', '').strip() or 'N/A'
            origin_country = item.get('origin_country', 'Unknown')
            velocity = item.get('velocity', 0.0) or 0.0
            # Предпочитаем baro_altitude, если есть, иначе geo_altitude
            altitude = item.get('baro_altitude') or item.get('geo_altitude') or 0.0
            on_ground = item.get('on_ground', True)

            a = Aeroplane(callsign, origin_country, velocity, altitude, on_ground)
            aeroplanes.append(a)
        except ValueError as e:
            # Если данные некорректны (например, отрицательная скорость), пропускаем объект
            print(f"Пропущен некорректный объект: {e}")

    print(f"Получено {len(aeroplanes)} записей о самолётах.")

    # 7. Сохранение в JSON-файл
    # Создаём папку data, если её нет
    import os
    os.makedirs('data', exist_ok=True)
    json_saver = JSONSaver('data/aeroplanes.json')
    for a in aeroplanes:
        json_saver.add_aeroplane(a)
    print(f"Данные сохранены в файл data/aeroplanes.json.")

    # 8. Фильтрация
    filtered_by_country = filter_by_origin_country(aeroplanes, filter_countries)
    filtered_by_altitude = filter_by_altitude_range(filtered_by_country, min_alt, max_alt)

    if not filtered_by_altitude:
        print("После применения фильтров не осталось самолётов для отображения.")
        return

    # 9. Сортировка и выбор топ-N
    sorted_aeroplanes = sort_by_altitude(filtered_by_altitude, reverse=True)
    top_aeroplanes = get_top_n(sorted_aeroplanes, top_n)

    # 10. Вывод результатов
    print(f"\n--- Топ {top_n} самолётов по высоте (после фильтрации) ---")
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()
