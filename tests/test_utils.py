# tests/test_utils.py
import pytest
from src.aeroplane import Aeroplane
from src.utils import (
    filter_by_origin_country,
    filter_by_altitude_range,
    filter_by_on_ground,
    sort_by_altitude,
    get_top_n,
    print_aeroplanes
)

class TestUtils:
    """Тесты для вспомогательных функций."""

    @pytest.fixture
    def sample_planes(self):
        return [
            Aeroplane("A", "USA", 200, 5000, False),
            Aeroplane("B", "Canada", 250, 7000, True),
            Aeroplane("C", "USA", 300, 6000, False),
            Aeroplane("D", "Mexico", 280, 8000, True),
            Aeroplane("E", "Canada", 220, 4000, False),
        ]

    def test_filter_by_origin_country(self, sample_planes):
        # Одна страна
        result = filter_by_origin_country(sample_planes, ["USA"])
        assert len(result) == 2
        assert all(p.origin_country == "USA" for p in result)

        # Несколько стран
        result = filter_by_origin_country(sample_planes, ["USA", "Canada"])
        assert len(result) == 4
        assert all(p.origin_country in {"USA", "Canada"} for p in result)

        # Пустой список
        result = filter_by_origin_country(sample_planes, [])
        assert result == sample_planes

        # Нет совпадений
        result = filter_by_origin_country(sample_planes, ["Germany"])
        assert result == []

    def test_filter_by_altitude_range(self, sample_planes):
        # Только нижняя граница
        result = filter_by_altitude_range(sample_planes, min_alt=6000, max_alt=None)
        assert len(result) == 3  # B(7000), C(6000), D(8000)
        assert all(p.altitude >= 6000 for p in result)

        # Только верхняя граница
        result = filter_by_altitude_range(sample_planes, min_alt=None, max_alt=6000)
        assert len(result) == 3  # A(5000), C(6000), E(4000)
        assert all(p.altitude <= 6000 for p in result)

        # Диапазон
        result = filter_by_altitude_range(sample_planes, min_alt=5000, max_alt=7000)
        assert len(result) == 3  # A(5000), B(7000), C(6000)
        assert all(5000 <= p.altitude <= 7000 for p in result)

        # Пустой диапазон
        result = filter_by_altitude_range(sample_planes, min_alt=10000, max_alt=20000)
        assert result == []

    def test_filter_by_on_ground(self, sample_planes):
        result = filter_by_on_ground(sample_planes, True)
        assert len(result) == 2  # B и D на земле
        assert all(p.on_ground is True for p in result)

        result = filter_by_on_ground(sample_planes, False)
        assert len(result) == 3
        assert all(p.on_ground is False for p in result)

    def test_sort_by_altitude(self, sample_planes):
        # По умолчанию убывание
        sorted_planes = sort_by_altitude(sample_planes)
        altitudes = [p.altitude for p in sorted_planes]
        assert altitudes == [8000, 7000, 6000, 5000, 4000]

        # По возрастанию
        sorted_planes_asc = sort_by_altitude(sample_planes, reverse=False)
        altitudes_asc = [p.altitude for p in sorted_planes_asc]
        assert altitudes_asc == [4000, 5000, 6000, 7000, 8000]

    def test_get_top_n(self, sample_planes):
        sorted_planes = sort_by_altitude(sample_planes)
        top2 = get_top_n(sorted_planes, 2)
        assert len(top2) == 2
        assert top2[0].altitude == 8000
        assert top2[1].altitude == 7000

        # Если n больше длины
        top10 = get_top_n(sorted_planes, 10)
        assert len(top10) == 5

    def test_print_aeroplanes(self, sample_planes, capsys):
        # Проверяем, что функция выводит что-то и не падает
        print_aeroplanes(sample_planes)
        captured = capsys.readouterr()
        assert "Позывной" in captured.out
        assert "A" in captured.out
        assert "Страна регистрации" in captured.out

        print_aeroplanes([])
        captured = capsys.readouterr()
        assert "Нет данных для отображения" in captured.out