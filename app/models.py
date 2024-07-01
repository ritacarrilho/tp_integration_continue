"""
Ce module définit les modèles de base de données pour l'application.
"""

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Task(Base): # pylint: disable=too-few-public-methods
    """
    Modèle représentant une tâche dans la base de données.
    
    Attributes:
        id (int): L'identifiant unique de la tâche.
        title (str): Le titre de la tâche.
        description (str): La description de la tâche.
        completed (bool): Indique si la tâche est terminée.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
