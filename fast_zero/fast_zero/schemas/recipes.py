from pydantic import BaseModel, ConfigDict


class RecipeSchema(BaseModel):
    id: int
    nome_refeicao: str
    nome_alimento: str
    nome_categoria: str
    quantidade: str
    kcal: int
    dia_semana: str
    model_config = ConfigDict(from_attributes=True)


class RecipeList(BaseModel):
    recipes: list[RecipeSchema]


class RecipeDB(RecipeSchema):
    id: int
