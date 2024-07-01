import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app import database, models, schemas

client = TestClient(app)

@pytest.fixture(scope='function')
def mock_db_session():
    with patch('app.database.SessionLocal') as mock_session_local:
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        yield mock_session

@pytest.fixture(scope='function', autouse=True)
def override_get_db(mock_db_session):
    def _get_db_override():
        try:
            yield mock_db_session
        finally:
            mock_db_session.close()

    app.dependency_overrides[database.get_db] = _get_db_override

def test_api_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

def test_create_task(mock_db_session):
    mock_task = models.Task(id=1, title="Test Task", description="Test Description", completed=False)
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    with patch('app.controllers.create_task', return_value=mock_task):
        response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"
        assert response.json()["description"] == "Test Description"
        assert response.json()["completed"] is False

def test_create_task_invalid(mock_db_session):
    response = client.post("/tasks/", json={})
    assert response.status_code == 422

def test_get_tasks(mock_db_session):
    mock_task = models.Task(id=1, title="Test Task", description="Test Description", completed=False)
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_task]

    with patch('app.controllers.get_tasks', return_value=[mock_task]):
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_get_task(mock_db_session):
    mock_task = models.Task(id=1, title="Another Task", description="Another Description", completed=False)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_task

    with patch('app.controllers.get_task', return_value=mock_task):
        response = client.get("/tasks/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

def test_get_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    with patch('app.controllers.get_task', return_value=None):
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

def test_update_task(mock_db_session):
    mock_task = models.Task(id=1, title="Updated Task", description="Updated Description", completed=True)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_task
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    with patch('app.controllers.update_task', return_value=mock_task):
        response = client.put("/tasks/1", json={"title": "Updated Task", "description": "Updated description", "completed": True})
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Task"
        assert response.json()["description"] == "Updated Description"
        assert response.json()["completed"] is True

def test_update_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    with patch('app.controllers.update_task', return_value=None):
        response = client.put("/tasks/999", json={"title": "Updated Task", "description": "Updated description", "completed": True})
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

def test_delete_task(mock_db_session):
    mock_task = models.Task(id=1, title="Delete Task", description="To be deleted", completed=False)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_task
    mock_db_session.commit.return_value = None

    with patch('app.controllers.delete_task', return_value=mock_task):
        response = client.delete("/tasks/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

def test_delete_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    with patch('app.controllers.delete_task', return_value=None):
        response = client.delete("/tasks/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}