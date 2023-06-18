from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
from alembic import command
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:data1base@localhost:5432/sm_api_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Test_SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.downgrade('base')
    # command.upgrade('head')
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@pytest.fixture(scope='function')
def client(session):   
    def overrider_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=overrider_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    userData={
        "email":"a@mail.com",
        "password":"1234"
    }
    res=client.post("/users/",json=userData)
    assert res.status_code == 201
    data=res.json()
    data['password']=userData['password']
    return data


@pytest.fixture
def get_token(test_user):
    return  create_access_token({'user_id':test_user['id']})


@pytest.fixture
def authorized_client(client,get_token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {get_token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session):
    posts=[{
        "title":"first title",
        "content":"first",
        "owner_id":test_user['id']
    },
    {
        "title":"second title",
        "content":"second",
        "owner_id":test_user['id']
    },
    {   
        "title":"second title",
        "content":"second",
        "owner_id":test_user['id']
    }]
    def create_post_db(post):
        return models.Post(**post)
    
    to_add_indb=list(map(create_post_db,posts))
    session.add_all(to_add_indb)
    session.commit()
    posts=session.query(models.Post).all()
    return posts
