from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models.models import RecipeModel, User


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
    }


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,
    }


def test_create_recipe(session, mock_db_time):
    new_recipe = RecipeModel(
        nome_refeicao='Almoço',
        nome_alimento='Abobrinha',
        nome_categoria='Pratos Únicos',
        quantidade='250g',
        kcal=300,
        dia_semana='Sábado',
    )
    session.add(new_recipe)
    session.commit()

    # Corrige a consulta para RecipeModel
    recipe = session.scalar(
        select(RecipeModel).where(RecipeModel.dia_semana == 'Sábado')
    )

    # Usa model_to_dict para converter recipe em um dicionário
    assert model_to_dict(recipe) == {
        'id': 1,
        'nome_refeicao': 'Almoço',
        'nome_alimento': 'Abobrinha',
        'nome_categoria': 'Pratos Únicos',
        'quantidade': '250g',
        'kcal': 300,
        'dia_semana': 'Sábado',
    }
