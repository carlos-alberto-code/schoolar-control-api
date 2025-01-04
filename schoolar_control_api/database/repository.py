from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import select, update, delete, and_
from typing import TypeVar, Generic, Type, Optional, List

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        """
        Inicializa el repositorio con el modelo y la sesión de la base de datos.

        :param model: Clase del modelo de SQLAlchemy.
        :param session: Sesión de SQLAlchemy.
        """
        self._model = model
        self._session = session

    def get(self, *conditions: ColumnElement[bool]) -> Optional[T]:
        """
        Recupera una única entidad basada en las condiciones proporcionadas.

        :param conditions: Condiciones para filtrar la consulta.
        :return: La entidad encontrada o None si no se encuentra ninguna.
        :raises RepositoryError: Si ocurre un error durante la consulta.

        Ejemplos:
            # Obtener por ID
            repo.get(User.id == 1)

            # Obtener con múltiples condiciones
            repo.get(User.email == "test@example.com", User.is_active == True)
        """
        try:
            stmt = select(self._model).where(and_(*conditions))
            result = self._session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise RepositoryError(f"Error retrieving {self._model.__name__}") from e

    def get_all(self, *conditions: ColumnElement[bool]) -> List[T]:
        """
        Recupera todas las entidades que coincidan con las condiciones proporcionadas.

        :param conditions: Condiciones para filtrar la consulta (opcional).
        :return: Lista de entidades encontradas.
        :raises RepositoryError: Si ocurre un error durante la consulta.

        Ejemplos:
            # Obtener todos los registros
            repo.get_all()

            # Obtener todos con condiciones
            repo.get_all(User.is_active == True)
        """
        try:
            stmt = select(self._model)
            if conditions:
                stmt = stmt.where(and_(*conditions))
            result = self._session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise RepositoryError(f"Error retrieving all {self._model.__name__}") from e

    def add(self, entity: T) -> T:
        """
        Añade una nueva entidad a la base de datos.

        :param entity: La entidad a añadir.
        :return: La entidad añadida con sus datos actualizados.
        :raises RepositoryError: Si ocurre un error durante la inserción.

        Ejemplos:
            user = User(name="John", email="john@example.com")
            repo.add(user)
        """
        try:
            self._session.add(entity)
            self._session.commit()
            self._session.flush()
            self._session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            raise RepositoryError(f"Error adding {self._model.__name__}") from e

    def update(self, *conditions: ColumnElement[bool], values: dict) -> Optional[T]:
        """
        Actualiza las entidades que coincidan con las condiciones proporcionadas con los valores dados.

        :param conditions: Condiciones para filtrar las entidades a actualizar.
        :param values: Diccionario con los valores a actualizar.
        :return: La entidad actualizada o None si no se encuentra ninguna.
        :raises RepositoryError: Si ocurre un error durante la actualización.

        Ejemplos:
            # Actualizar por ID
            repo.update(User.id == 1, values={"name": "New Name"})

            # Actualizar con múltiples condiciones
            repo.update(
                User.email == "test@example.com",
                User.is_active == True,
                values={"status": "updated"}
            )
        """
        try:
            combined_conditions = and_(*conditions)
            stmt = (
                update(self._model)
                .where(combined_conditions)
                .values(**values)
                .returning(self._model)
            )
            result = self._session.execute(stmt)
            self._session.commit()
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise RepositoryError(f"Error updating {self._model.__name__}") from e

    def delete(self, *conditions: ColumnElement[bool]) -> bool:
        """
        Elimina las entidades que coincidan con las condiciones proporcionadas.

        :param conditions: Condiciones para filtrar las entidades a eliminar.
        :return: True si se eliminó al menos una entidad, False en caso contrario.
        :raises RepositoryError: Si ocurre un error durante la eliminación.

        Ejemplos:
            # Eliminar por ID
            repo.delete(User.id == 1)

            # Eliminar con múltiples condiciones
            repo.delete(User.email == "test@example.com", User.is_active == False)
        """
        try:
            stmt = delete(self._model).where(and_(*conditions))
            result = self._session.execute(stmt)
            self._session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            raise RepositoryError(f"Error deleting {self._model.__name__}") from e


class RepositoryError(Exception):
    """Excepción base para errores del repositorio"""

    pass
