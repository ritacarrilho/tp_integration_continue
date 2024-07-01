import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app import models, schemas, controllers

@pytest.fixture
def mock_db_session():
    with patch('app.database.SessionLocal') as mock_session_local:
        mock_session = MagicMock(spec=Session)
        mock_session_local.return_value = mock_session
        yield mock_session

def test_get_task(mock_db_session):
    mock_task = models.Task(id=1, title="Test Task", description="Test Description", completed=False)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_task

    task = controllers.get_task(mock_db_session, task_id=1)
    assert task == mock_task
    mock_db_session.query.assert_called_once_with(models.Task)
    filter_args, _ = mock_db_session.query.return_value.filter.call_args
    assert filter_args[0].compare(models.Task.id == 1)

def test_get_tasks(mock_db_session):
    mock_tasks = [
        models.Task(id=1, title="Test Task 1", description="Test Description 1", completed=False),
        models.Task(id=2, title="Test Task 2", description="Test Description 2", completed=False)
    ]
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_tasks

    tasks = controllers.get_tasks(mock_db_session, skip=0, limit=10)
    assert tasks == mock_tasks
    mock_db_session.query.assert_called_once_with(models.Task)

def test_create_task(mock_db_session):
    task_create = schemas.TaskCreate(title="New Task", description="New Description", completed=False)
    mock_task = models.Task(id=1, title="New Task", description="New Description", completed=False)
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    with patch('app.models.Task', return_value=mock_task):
        created_task = controllers.create_task(mock_db_session, task_create)
        assert created_task == mock_task
        mock_db_session.add.assert_called_once_with(mock_task)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_task)

def test_delete_task(mock_db_session):
    mock_task = models.Task(id=1, title="Task to Delete", description="To be deleted", completed=False)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_task

    deleted_task = controllers.delete_task(mock_db_session, task_id=1)
    assert deleted_task == mock_task
    mock_db_session.delete.assert_called_once_with(mock_task)
    mock_db_session.commit.assert_called_once()

def test_delete_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    deleted_task = controllers.delete_task(mock_db_session, task_id=999)
    assert deleted_task is None
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()

def test_update_task(mock_db_session):
    mock_task = models.Task(id=1, title="Old Task", description="Old Description", completed=False)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_task
    updated_task = schemas.TaskCreate(title="Updated Task", description="Updated Description", completed=True)

    result_task = controllers.update_task(mock_db_session, task_id=1, updated_task=updated_task)
    assert result_task == mock_task
    assert mock_task.title == updated_task.title
    assert mock_task.description == updated_task.description
    assert mock_task.completed == updated_task.completed
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_task)

def test_update_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    updated_task = schemas.TaskCreate(title="Updated Task", description="Updated Description", completed=True)

    result_task = controllers.update_task(mock_db_session, task_id=999, updated_task=updated_task)
    assert result_task is None
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()