"""
Ce module définit les points de terminaison de l'API FastAPI pour gérer les tâches.
Il inclut des opérations pour créer, lire, mettre à jour et supprimer des tâches.
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas, controllers
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Tasks Api",
    description="Tasks Api créée pour un projet d'intégration continue",
    summary="L'application préférée de Deadpool. Assez dit.",
    version="0.0.1",
)

@app.get("/", response_model=dict, tags=["Health Check"])
def api_status():
    """
    Vérifie l'état de l'API.

    Returns:
        dict: Un dictionnaire avec le statut de l'API.
    """
    return {"status": "running"}

@app.post("/tasks/", response_model=schemas.Task, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle tâche.

    Args:
        task (schemas.TaskCreate): Les données de la tâche à créer.
        db (Session): La session de la base de données.

    Returns:
        schemas.Task: La tâche créée.
    """
    return controllers.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tasks"])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère une liste de tâches avec pagination.

    Args:
        skip (int): Le nombre de tâches à ignorer. Par défaut, 0.
        limit (int): Le nombre maximum de tâches à retourner. Par défaut, 10.
        db (Session): La session de la base de données.

    Returns:
        List[schemas.Task]: Une liste de tâches.
    """
    return controllers.get_tasks(db=db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Récupère une tâche par son ID.

    Args:
        task_id (int): L'ID de la tâche à récupérer.
        db (Session): La session de la base de données.

    Raises:
        HTTPException: Si la tâche n'est pas trouvée.

    Returns:
        schemas.Task: La tâche trouvée.
    """
    db_task = controllers.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Met à jour une tâche existante.

    Args:
        task_id (int): L'ID de la tâche à mettre à jour.
        updated_task (schemas.TaskCreate): Les nouvelles données de la tâche.
        db (Session): La session de la base de données.

    Raises:
        HTTPException: Si la tâche n'est pas trouvée.

    Returns:
        schemas.Task: La tâche mise à jour.
    """
    db_task = controllers.update_task(db, task_id=task_id, updated_task=updated_task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Supprime une tâche par son ID.

    Args:
        task_id (int): L'ID de la tâche à supprimer.
        db (Session): La session de la base de données.

    Raises:
        HTTPException: Si la tâche n'est pas trouvée.

    Returns:
        schemas.Task: La tâche supprimée.
    """
    db_task = controllers.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
