from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    # Exercício
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class RecipeModel:
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_refeicao: Mapped[str]
    nome_alimento: Mapped[str]
    nome_categoria: Mapped[str]
    quantidade: Mapped[str]
    kcal: Mapped[int]
    dia_semana: Mapped[str]
  
