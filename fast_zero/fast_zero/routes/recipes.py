from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from fast_zero.schemas.recipes import Recipe, RecipeList
from fast_zero.schemas.users import Message

router = APIRouter(
    prefix='/receitas',
    tags=['Receitas'],
)

database = []


@router.post(
    '/recipes/', status_code=HTTPStatus.CREATED, response_model=Recipe
)
def create_recipe(recipe: Recipe):
    recipe_data = Recipe(**recipe.model_dump())
    database.append(recipe_data)

    return recipe_data


@router.get('/recipes/', response_model=RecipeList)
def read_recipes():
    return {'recipes': database}


@router.put('/recipes/{recipe_id}', response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe):
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
def delete_recipe(recipe_id: int):
    if recipe_id < 1 or recipe_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Recipe not found'
        )

    del database[recipe_id - 1]

    return {'message': 'Recipe deleted successfully'}
