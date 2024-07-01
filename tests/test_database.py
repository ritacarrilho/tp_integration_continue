import pytest
import os
import importlib
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db, DATABASE_URL


def test_database_url():
    from app.database import DATABASE_URL
    assert DATABASE_URL == 'postgresql://taskuser:taskpassword@tasks-db/taskdb'


def test_get_db():
    mock_session = MagicMock()
    with patch('app.database.SessionLocal', return_value=mock_session):
        gen = get_db()
        db = next(gen)
        assert db == mock_session
        mock_session.close.assert_not_called() 
        try:
            next(gen)
        except StopIteration:
            pass
        mock_session.close.assert_called_once()