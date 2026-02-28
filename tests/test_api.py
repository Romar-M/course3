# tests/test_api.py
import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from src.api import AeroplanesAPI


class TestAeroplanesAPI:
    """Тесты для класса AeroplanesAPI с моками запросов."""

    @patch('src.api.requests.Session.get')
    def test_get_boundingbox_success(self, mock_get):
        # Настраиваем mock для ответа Nominatim
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "boundingbox": ["41.6765597", "83.3362128", "-141.0027500", "-52.3237664"]
            }
        ]
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        bbox = api._get_boundingbox("Canada")
        assert bbox == (41.6765597, 83.3362128, -141.00275, -52.3237664)

        # Проверяем, что запрос был сделан с правильными параметрами
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['country'] == "Canada"
        assert kwargs['headers'] == {'User-Agent': 'aeroplane-project/1.0'}

    @patch('src.api.requests.Session.get')
    def test_get_boundingbox_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []  # пустой ответ
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        bbox = api._get_boundingbox("Atlantis")
        assert bbox is None

    @patch('src.api.requests.Session.get')
    def test_get_boundingbox_http_error(self, mock_get):
        # Используем исключение из библиотеки requests
        mock_get.side_effect = requests.ConnectionError("Connection error")

        api = AeroplanesAPI()
        bbox = api._get_boundingbox("Canada")
        assert bbox is None

    @patch('src.api.AeroplanesAPI._connect')
    def test_get_aeroplanes_success(self, mock_connect):
        # Мокаем _connect для двух вызовов
        # Первый вызов (Nominatim) возвращает boundingbox
        mock_connect.side_effect = [
            # результат первого вызова (nominatim)
            [
                {
                    "boundingbox": ["41.6765597", "83.3362128", "-141.0027500", "-52.3237664"]
                }
            ],
            # результат второго вызова (opensky)
            {
                "states": [
                    ["abc123", "UAL123", "United States", 123456, 123456,
                     -100.5, 40.5, 10000.0, False, 250.0, 120.0, 0.0,
                     None, 10100.0, "1234", False, 0]
                ]
            }
        ]

        api = AeroplanesAPI()
        result = api.get_aeroplanes("Canada")

        assert len(result) == 1
        assert result[0]['icao24'] == "abc123"
        assert result[0]['callsign'] == "UAL123"
        assert result[0]['origin_country'] == "United States"
        assert result[0]['velocity'] == 250.0

        # Должно быть два вызова _connect
        assert mock_connect.call_count == 2

    @patch('src.api.AeroplanesAPI._connect')
    def test_get_aeroplanes_no_boundingbox(self, mock_connect):
        # Первый вызов возвращает None (страна не найдена)
        mock_connect.return_value = None

        api = AeroplanesAPI()
        result = api.get_aeroplanes("Unknown")
        assert result == []
        mock_connect.assert_called_once()

    @patch('src.api.AeroplanesAPI._connect')
    def test_get_aeroplanes_opensky_empty(self, mock_connect):
        # Первый вызов успешен, второй возвращает None
        mock_connect.side_effect = [
            [{"boundingbox": ["1", "2", "3", "4"]}],
            None
        ]

        api = AeroplanesAPI()
        result = api.get_aeroplanes("Canada")
        assert result == []
        assert mock_connect.call_count == 2

    def test_connect_method_with_auth(self):
        # Тестируем, что при наличии логина/пароля устанавливается аутентификация
        with patch('src.api.requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session
            api = AeroplanesAPI(username="user", password="pass")
            assert mock_session.auth == ("user", "pass")