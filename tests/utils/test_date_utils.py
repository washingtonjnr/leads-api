import pytest

from app.utils.date import format_date

class TestDateUtils:
    def test_format_date_valid_string(self):
        result = format_date("1990-05-15")
        assert result == "15/05/1990"
    
    def test_format_date_different_format(self):
        result = format_date("1990-05-15")
        assert isinstance(result, str)
    
    def test_format_date_returns_string(self):
        result = format_date("2000-01-01")
        assert isinstance(result, str)
