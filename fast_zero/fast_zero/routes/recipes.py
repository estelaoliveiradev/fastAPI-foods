from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database.database import get_session
from fast_zero.models.models import RecipeModel
from fast_zero.schemas.recipes import Recipe, RecipeList
from fast_zero.schemas.users import Message

router = APIRouter(
    prefix='/receitas',
    tags=['Receitas'],
)

database = []


@router.post(
    '/recipes/', status_code=HTTPStatus.CREATED, response_model=RecipeModel
)
def create_recipe(recipe: Recipe, session: Session = Depends(get_session)):
    db_recipe = session.scalar(
        select(Recipe).where(
            (Recipe.nome_refeicao == recipe.nome_refeicao)
            | (Recipe.nome_alimento == recipe.nome_alimento)
        )
    )

    if db_recipe:
        if db_recipe.nome_refeicao == recipe.nome_refeicao:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='nome_refeicao already exists',
            )
        elif db_recipe.nome_alimento == recipe.nome_alimento:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='nome_alimento already exists',
            )

    db_recipe = Recipe(
        nome_refeicao=recipe.nome_refeicao,
        password=recipe.password,
        nome_alimento=recipe.nome_alimento,
    )
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)

    return db_recipe


@router.get('/recipes/', response_model=RecipeList)
def read_recipes(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    recipes = session.scalars(select(Recipe).offset(skip).limit(limit)).all()
    return {'recipes': recipes}


@router.put('/recipes/{recipe_id}', response_model=Recipe)
def update_recipe(
    recipe_id: int, recipe: Recipe, session: Session = Depends(get_session)
):
    if recipe_id < 1 or recipe_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Recipe not found'
        )

    existing_recipe = database[recipe_id - 1]
    updated_recipe_data = recipe.model_dump()

    for key, value in updated_recipe_data.items():
        setattr(existing_recipe, key, value)

    return existing_recipe


@router.delete('/recipes/{recipe_id}', response_model=Message)
def delete_recipe(recipe_id: int, session: Session = Depends(get_session)):
    if recipe_id < 1 or recipe_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Recipe not found'
        )

    del database[recipe_id - 1]

    return {'message': 'Recipe deleted successfully'}
