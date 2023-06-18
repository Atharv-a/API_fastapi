from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
from alembic import command

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

