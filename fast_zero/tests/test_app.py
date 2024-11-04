from http import HTTPStatus

from fastapi import FastAPI
from fastapi.testclient import TestClient

# Suponha que você tenha uma aplicação FastAPI chamada 'app'
app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Olá Mundo!'}


client = TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
