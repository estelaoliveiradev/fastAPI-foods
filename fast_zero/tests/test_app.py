from http import HTTPStatus

from fastapi import FastAPI

from tests.router import recipes, users

# Suponha que você tenha uma aplicação FastAPI chamada 'app'
app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Olá Mundo!'}




def test_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}

app.include_router(recipes.router)
app.include_router(users.router)
