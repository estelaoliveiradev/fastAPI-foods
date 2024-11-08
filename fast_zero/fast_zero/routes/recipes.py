from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database.database import get_session
from fast_zero.models.models import RecipeModel
from fast_zero.schemas.recipes import RecipeList, RecipeSchema
from fast_zero.schemas.users import Message

router = APIRouter(
    prefix='/receitas',
    tags=['Receitas'],
)

database = []


@router.post(
    '/recipes/', status_code=HTTPStatus.CREATED, response_model=RecipeModel
)
def create_recipe(
    recipe: RecipeSchema, session: Session = Depends(get_session)):
    db_recipe = session.scalar(
        select(RecipeModel).where(
            (RecipeModel.nome_alimento == recipe.nome_alimento)
        )
    )

    if db_recipe:
        if db_recipe.nome_alimento == recipe.nome_alimento:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='nome_alimento already exists',
            )

    db_recipe = RecipeModel(
        nome_refeicao=recipe.nome_refeicao,
        nome_alimento=recipe.nome_alimento,
        nome_categoria=recipe.nome_categoria,
        quantidade=recipe.quantidade,
        kcal=recipe.kcal,
        dia_semana=recipe.dia_semana
    )
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)

    return db_recipe


@router.get('/recipes/', response_model=RecipeList)
def read_recipes(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    recipes = session.scalars(select
        (RecipeModel).offset(skip).limit(limit)).all()
    return {'recipes': recipes}


@router.put('/recipes/{recipe_id}', response_model=RecipeSchema)
def update_recipe(
    recipe_id: int,
    recipe: RecipeSchema,
    session: Session = Depends(get_session)
):
    db_recipe = session.scalar(
        select(RecipeModel).where(RecipeModel.id == recipe_id)
    )
    if not db_recipe:
        raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Recipe not found'
    )
    db_recipe.nome_refeicao = recipe.nome_refeicao
    db_recipe.nome_alimento = recipe.nome_alimento
    db_recipe.nome_categoria = recipe.nome_categoria
    db_recipe.quantidade = recipe.quantidade
    db_recipe.kcal = recipe.kcal
    db_recipe.dia_semana = recipe.dia
    session.commit()
    session.refresh(db_recipe)

    return db_recipe


@router.delete('/recipes/{recipe_id}', response_model=Message)
def delete_recipe(recipe_id: int, session: Session = Depends(get_session)):

    db_recipe = select(
        select(RecipeModel).where(RecipeModel.id == recipe_id)

    )
    if not db_recipe:
        raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Recipe not found'
    )

    session.delete()
    session.commit()

    return {'message': 'Recipe deleted'}
