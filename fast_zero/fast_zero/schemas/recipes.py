from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    nome_refeicao: str
    nome_alimento: str
    nome_categoria: str
    quantidade: str
    kcal: int
    dia_semana: str
    message: str


class RecipeList(BaseModel):
    users: list[Recipe]


class RecipeDB(Recipe):
    id: int
