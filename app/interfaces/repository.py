from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")

class IBaseRepository(Generic[T], ABC):
    """
    Dependency Inversion (DIP) & Reusability:
    Generic repository abstraction decoupling data access from business domain logic.
    """
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass
