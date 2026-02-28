# tests/test_storage.py
import pytest
import json
import os
from src.aeroplane import Aeroplane
from src.storage import JSONSaver


class TestJSONSaver:
    """Тесты для класса JSONSaver."""

    def test_init_creates_file_if_not_exists(self, tmp_path):
        file_path = tmp_path / "test.json"
        assert not file_path.exists()
        saver = JSONSaver(str(file_path))
        assert file_path.exists()
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data == []

    def test_add_and_get_all(self, tmp_path):
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))
        a1 = Aeroplane("TEST1", "USA", 250, 10000, False)
        a2 = Aeroplane("TEST2", "Canada", 300, 12000, True)

        saver.add_aeroplane(a1)
        saver.add_aeroplane(a2)

        all_planes = saver.get_aeroplanes()
        assert len(all_planes) == 2
        # Проверяем, что данные соответствуют
        callsigns = {p['callsign'] for p in all_planes}
        assert callsigns == {"TEST1", "TEST2"}

    def test_add_duplicate(self, tmp_path):
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))
        a = Aeroplane("TEST1", "USA", 250, 10000, False)

        saver.add_aeroplane(a)
        saver.add_aeroplane(a)  # второй раз

        all_planes = saver.get_aeroplanes()
        assert len(all_planes) == 1  # дубликат не добавился

    def test_get_with_filter(self, tmp_path):
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))
        a1 = Aeroplane("TEST1", "USA", 250, 10000, False)
        a2 = Aeroplane("TEST2", "Canada", 300, 12000, True)
        a3 = Aeroplane("TEST3", "USA", 280, 9000, True)

        saver.add_aeroplane(a1)
        saver.add_aeroplane(a2)
        saver.add_aeroplane(a3)

        # Фильтр по стране
        usa_planes = saver.get_aeroplanes(origin_country="USA")
        assert len(usa_planes) == 2
        for p in usa_planes:
            assert p['origin_country'] == "USA"

        # Фильтр по состоянию на земле
        on_ground = saver.get_aeroplanes(on_ground=True)
        assert len(on_ground) == 2
        for p in on_ground:
            assert p['on_ground'] is True

        # Комбинированный фильтр
        usa_on_ground = saver.get_aeroplanes(origin_country="USA", on_ground=True)
        assert len(usa_on_ground) == 1
        assert usa_on_ground[0]['callsign'] == "TEST3"

    def test_delete_with_criteria(self, tmp_path):
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))
        a1 = Aeroplane("TEST1", "USA", 250, 10000, False)
        a2 = Aeroplane("TEST2", "Canada", 300, 12000, True)
        a3 = Aeroplane("TEST3", "USA", 280, 9000, True)

        saver.add_aeroplane(a1)
        saver.add_aeroplane(a2)
        saver.add_aeroplane(a3)

        # Удаляем самолёты из США
        saver.delete_aeroplane(origin_country="USA")
        remaining = saver.get_aeroplanes()
        assert len(remaining) == 1
        assert remaining[0]['origin_country'] == "Canada"

        # Проверяем, что файл обновился
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]['callsign'] == "TEST2"

    def test_delete_no_criteria_does_nothing(self, tmp_path):
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))
        a = Aeroplane("TEST1", "USA", 250, 10000, False)
        saver.add_aeroplane(a)

        saver.delete_aeroplane()  # без критериев
        remaining = saver.get_aeroplanes()
        assert len(remaining) == 1  # ничего не удалилось

    def test_get_empty_criteria_returns_all(self, tmp_path):
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))
        a = Aeroplane("TEST1", "USA", 250, 10000, False)
        saver.add_aeroplane(a)

        all_planes = saver.get_aeroplanes()  # без критериев
        assert len(all_planes) == 1
