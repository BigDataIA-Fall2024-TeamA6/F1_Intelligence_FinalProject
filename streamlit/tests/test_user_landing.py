import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from F1_Intelligence_FinalProject.streamlit.pages.user_landing import get_race_calendar, get_driver_standings, get_constructor_standings

@pytest.fixture
def mock_mysql_connector():
    with patch('user_landing.mysql.connector') as mock_connector:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connector.connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        yield mock_connector

def test_get_race_calendar(mock_mysql_connector):
    mock_cursor = mock_mysql_connector.connect().cursor()
    mock_cursor.fetchall.return_value = [
        {'Grand Prix': 'Bahrain', 'Venue': 'Bahrain International Circuit', 'Dates': 'March 2-3'},
        {'Grand Prix': 'Saudi Arabia', 'Venue': 'Jeddah Corniche Circuit', 'Dates': 'March 9-10'}
    ]

    result = get_race_calendar()

    assert isinstance(result, dict)
    assert 'Grand Prix' in result
    assert 'Venue' in result
    assert 'Dates' in result
    assert len(result['Grand Prix']) == 2
    assert result['Grand Prix'][0] == 'Bahrain'
    assert result['Venue'][1] == 'Jeddah Corniche Circuit'

def test_get_driver_standings(mock_mysql_connector):
    mock_cursor = mock_mysql_connector.connect().cursor()
    mock_cursor.fetchall.return_value = [
        {'Pos': '1', 'Driver': 'Max Verstappen', 'Nationality': 'Dutch', 'Car': 'Red Bull Racing', 'Pts': '575'},
        {'Pos': '2', 'Driver': 'Lewis Hamilton', 'Nationality': 'British', 'Car': 'Mercedes', 'Pts': '490'}
    ]

    result = get_driver_standings()

    assert isinstance(result, dict)
    assert 'Pos' in result
    assert 'Driver' in result
    assert 'Nationality' in result
    assert 'Car' in result
    assert 'Pts' in result
    assert len(result['Pos']) == 2
    assert result['Driver'][0] == 'Max Verstappen'
    assert result['Pts'][1] == '490'

def test_get_constructor_standings(mock_mysql_connector):
    mock_cursor = mock_mysql_connector.connect().cursor()
    mock_cursor.fetchall.return_value = [
        {'Pos': '1', 'Team': 'Red Bull Racing', 'Pts': '860'},
        {'Pos': '2', 'Team': 'Mercedes', 'Pts': '710'}
    ]

    result = get_constructor_standings()

    assert isinstance(result, dict)
    assert 'Pos' in result
    assert 'Team' in result
    assert 'Pts' in result
    assert len(result['Pos']) == 2
    assert result['Team'][0] == 'Red Bull Racing'
    assert result['Pts'][1] == '710'
