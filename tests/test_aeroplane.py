# tests/test_aeroplane.py
import pytest
from src.aeroplane import Aeroplane

class TestAeroplane:
    """Тесты для класса Aeroplane."""

    def test_valid_creation(self):
        a = Aeroplane("TEST123", "Canada", 300.0, 12000.0, True)
        assert a.callsign == "TEST123"
        assert a.origin_country == "Canada"
        assert a.velocity == 300.0
        assert a.altitude == 12000.0
        assert a.on_ground is True

    def test_callsign_strip(self):
        a = Aeroplane("  TEST  ", "USA", 100, 5000, False)
        assert a.callsign == "TEST"

    def test_invalid_callsign_empty(self):
        with pytest.raises(ValueError, match="callsign must be a non-empty string"):
            Aeroplane("", "USA", 100, 5000, False)

    def test_invalid_callsign_not_string(self):
        with pytest.raises(ValueError, match="callsign must be a non-empty string"):
            Aeroplane(123, "USA", 100, 5000, False)  # type: ignore

    def test_negative_velocity(self):
        with pytest.raises(ValueError, match="velocity cannot be negative"):
            Aeroplane("TEST", "USA", -10, 5000, False)

    def test_velocity_not_number(self):
        with pytest.raises(ValueError, match="velocity must be a number"):
            Aeroplane("TEST", "USA", "fast", 5000, False)  # type: ignore

    def test_negative_altitude(self):
        with pytest.raises(ValueError, match="altitude cannot be negative"):
            Aeroplane("TEST", "USA", 100, -500, False)

    def test_on_ground_not_bool(self):
        with pytest.raises(ValueError, match="on_ground must be a boolean"):
            Aeroplane("TEST", "USA", 100, 5000, "yes")  # type: ignore

    def test_comparison_lt(self):
        a1 = Aeroplane("A", "USA", 200, 8000, False)
        a2 = Aeroplane("B", "USA", 250, 10000, False)
        assert a1 < a2
        assert not (a2 < a1)

    def test_comparison_le(self):
        a1 = Aeroplane("A", "USA", 200, 8000, False)
        a2 = Aeroplane("B", "USA", 250, 8000, False)
        a3 = Aeroplane("C", "USA", 300, 10000, False)
        assert a1 <= a2
        assert a2 <= a1
        assert a1 <= a3

    def test_comparison_eq(self):
        a1 = Aeroplane("A", "USA", 200, 8000, False)
        a2 = Aeroplane("B", "USA", 250, 8000, False)
        a3 = Aeroplane("C", "USA", 200, 8000, False)
        assert a1 == a2
        assert a1 == a3
        assert not (a1 == "not aeroplane")

    def test_compare_speed(self):
        a1 = Aeroplane("A", "USA", 200, 8000, False)
        a2 = Aeroplane("B", "USA", 250, 10000, False)
        a3 = Aeroplane("C", "USA", 200, 9000, False)
        assert a1.compare_speed(a2) == -1
        assert a2.compare_speed(a1) == 1
        assert a1.compare_speed(a3) == 0

    def test_to_dict(self):
        a = Aeroplane("TEST", "France", 280.5, 9500.0, False)
        d = a.to_dict()
        assert d == {
            'callsign': 'TEST',
            'origin_country': 'France',
            'velocity': 280.5,
            'altitude': 9500.0,
            'on_ground': False
        }

    def test_from_dict(self):
        data = {
            'callsign': 'TEST',
            'origin_country': 'France',
            'velocity': 280.5,
            'altitude': 9500.0,
            'on_ground': False
        }
        a = Aeroplane.from_dict(data)
        assert a.callsign == 'TEST'
        assert a.origin_country == 'France'
        assert a.velocity == 280.5
        assert a.altitude == 9500.0
        assert a.on_ground is False

    def test_repr(self):
        a = Aeroplane("TEST", "France", 280.5, 9500.0, False)
        repr_str = repr(a)
        assert "Aeroplane" in repr_str
        assert "TEST" in repr_str
