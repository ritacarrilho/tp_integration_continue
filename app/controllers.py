"""
Ce module fournit les contrôleurs pour gérer les opérations de tâches.
Il comprend des fonctions pour obtenir, créer, supprimer et mettre à jour des tâches dans la bdd.
"""

from sqlalchemy.orm import Session
from . import models, schemas

def get_task(db: Session, task_id: int):
    """
    Récupère une tâche par son ID.

    Args:
        db (Session): La session de la base de données.
        task_id (int): L'ID de la tâche à récupérer.

    Returns:
        Task: L'objet tâche si trouvé, sinon None.
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    """
    Récupère une liste de tâches avec pagination optionnelle.

    Args:
        db (Session): La session de la base de données.
        skip (int): Le nombre de tâches à ignorer. Par défaut, 0.
        limit (int): Le nombre maximum de tâches à retourner. Par défaut, 10.

    Returns:
        List[Task]: Une liste d'objets tâche.
    """
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    """
    Crée une nouvelle tâche dans la base de données.

    Args:
        db (Session): La session de la base de données.
        task (schemas.TaskCreate): Les données de la tâche à créer.

    Returns:
        Task: L'objet tâche créé.
    """
    db_task = models.Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """
    Supprime une tâche par son ID.

    Args:
        db (Session): La session de la base de données.
        task_id (int): L'ID de la tâche à supprimer.

    Returns:
        Task: L'objet tâche supprimé si trouvé, sinon None.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def update_task(db: Session, task_id: int, updated_task: schemas.TaskCreate):
    """
    Met à jour une tâche existante par son ID.

    Args:
        db (Session): La session de la base de données.
        task_id (int): L'ID de la tâche à mettre à jour.
        updated_task (schemas.TaskCreate): Les nouvelles données de la tâche.

    Returns:
        Task: L'objet tâche mis à jour si trouvé, sinon None.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.title = updated_task.title
        db_task.description = updated_task.description
        db_task.completed = updated_task.completed
        db.commit()
        db.refresh(db_task)
    return db_task
