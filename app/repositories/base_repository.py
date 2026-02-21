from typing import Generic, TypeVar, Type, Any, List, Dict


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update



from ..core import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        Инициализация репозитория с конкретной ORM-моделью.
        """
        self._model = model

    async def get_by_id(self, session: AsyncSession, pk: Any) -> ModelType | None:
        """
        Получает запись по первичному ключу.
        """
        # SQLAlchemy 2.0 style: select(Model)
        stmt = select(self._model).where(self._model.id == pk)
        
        # .scalar_one_or_none() возвращает сам объект или None
        result = await session.scalar(stmt)
        return result

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        """
        Получает все записи модели.
        """
        stmt = select(self._model)
        
        # .scalars() возвращает список объектов модели
        result = await session.scalars(stmt)
        return list(result.all())

    async def create(self, session: AsyncSession, data: Dict[str, Any]) -> ModelType:
        """
        Создает новую запись в БД.
        :param data: Словарь данных (например, .model_dump() из Pydantic)
        """
        # Создаем экземпляр модели из данных
        db_object = self._model(**data)
        
        session.add(db_object)
        
        # Сохраняем изменения и ждем ID
        await session.commit()
        await session.refresh(db_object) 
        
        return db_object

    async def update(self, session: AsyncSession, pk: Any, data: Dict[str, Any]) -> ModelType | None:
        """
        Обновляет запись по первичному ключу.
        """
        # 1. Сначала находим объект
        db_object = await self.get_by_id(session, pk)
        
        if not db_object:
            return None

        # 2. Применяем изменения к объекту
        for key, value in data.items():
            if hasattr(db_object, key) and value is not None:
                 setattr(db_object, key, value)
                 
        # 3. Сохраняем и обновляем
        await session.commit()
        await session.refresh(db_object)
        
        return db_object


    async def delete(self, session: AsyncSession, pk: Any) -> bool:
        """
        Удаляет запись по первичному ключу.
        """
        stmt = delete(self._model).where(self._model.id == pk)
        
        result = await session.execute(stmt)
        
        # commit не обязателен, т.к. session.execute() выполняет DML.
        # Но для завершения транзакции и записи изменений в БД нужен commit.
        await session.commit() 
        
        # rowcount > 0 означает, что что-то было удалено
        return result.rowcount > 0