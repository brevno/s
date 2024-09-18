import pytest
from fastapi.testclient import TestClient
from main import app
from server.db import db_session_default_params
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[db_session_default_params] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create the database tables
    from server.db import Base
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)

def test_create_short_url(setup_database):
    response = client.post("/create", json={"url": "http://example.com", "expiration_hrs": 0})
    assert response.status_code == 200
    assert "short_url" in response.json()

def test_create_short_url_with_expiration(setup_database):
    response = client.post("/create", json={"url": "http://example.com", "expiration_hrs": 1})
    assert response.status_code == 200
    assert "short_url" in response.json()

def test_follow_shortlink(setup_database):
    # Create a short link first
    response = client.post("/create", json={"url": "http://example.com", "expiration_hrs": 0})
    short_url = response.json()["short_url"]
    hash = short_url.split("/")[-1]

    # Follow the short link
    response = client.get(f"/{hash}")
    assert response.status_code == 200
    assert str(response.url) == "http://example.com/"

def test_follow_shortlink_not_found(setup_database):
    response = client.get("/invalidhash")
    assert response.status_code == 404

def test_follow_shortlink_expired(setup_database):
    # Create a short link with expiration
    response = client.post("/create", json={"url": "http://example.com", "expiration_hrs": -1})
    short_url = response.json()["short_url"]
    hash = short_url.split("/")[-1]

    # Follow the short link
    response = client.get(f"/{hash}")
    assert response.status_code == 410