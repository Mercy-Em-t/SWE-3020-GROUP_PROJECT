from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.interfaces.repository import IBaseRepository

ModelType = TypeVar("ModelType")

class BaseRepository(IBaseRepository[ModelType], Generic[ModelType]):
    """Generic repository implementation for SQLAlchemy."""
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == entity_id).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, entity: ModelType) -> ModelType:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
