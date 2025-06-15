import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_utils import Base, get_db
from main import app, update_user_streak, calculate_milestone_bonus
from models import User, CheckIn

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database once for all tests."""

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    """Create a single test client for all tests."""
    return TestClient(app)


@pytest.fixture
def clean_db():
    """Clean database between tests that need isolation."""
    db = TestingSession()
    try:
        # Delete all records (keeping tables)
        db.query(CheckIn).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


class TestBasicFunctionality:

    def test_if_user_created_successfully_return_200(self, client, clean_db):
        """Test user creation."""

        user_data = {"username": "newuser", "email": "new@gmail.com"}

        response = client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert data["current_streak"] == 0
        assert data["total_xp"] == 0

    def test_if_user_already_exists_return_400(self, client, clean_db):
        """Test user creation with duplicate username or email."""
        user_data = {"username": "duplicate", "email": "duplicate@gmail.com"}

        # Create the user for the first time
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == status.HTTP_200_OK

        # Try to create the same user again
        response2 = client.post("/users/", json=user_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST


class TestCheckInFunctionality:

    def test_if_check_in_successful_return_200(self, client):
        """Test successful check-in."""
        user_data = {"username": "checkinuser", "email": "checkin@gmail.com"}

        # Create a user
        user_response = client.post("/users/", json=user_data)
        user = user_response.json()

        # Create a check-in for the user
        checkin_data = {"user_id": user["id"]}
        checkin_response = client.post("/checkin/", json=checkin_data)

        assert checkin_response.status_code == status.HTTP_200_OK
        data = checkin_response.json()
        assert data["success"] == True

    def test_if_check_in_twice_on_same_day_returns_400(self, client):
        """Test check-in on the same day."""
        user_data = {"username": "twiceuser", "email": "twice@gamil.com"}

        # Create a user
        user_response = client.post("/users/", json=user_data)
        user = user_response.json()

        checkin_data = {"user_id": user["id"]}

        # Frist check-in should succeed
        response1 = client.post("/checkin/", json=checkin_data)
        assert response1.status_code == status.HTTP_200_OK

        # Second check-in on the same day should fail
        response2 = client.post("/checkin/", json=checkin_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_not_exists_return_404(self, client):
        """Test check-in for a non-existent user."""
        checkin_data = {
            "user_id": 9999}  # Assuming this user ID does not exist

        response = client.post("/checkins/", json=checkin_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestStreakLogic:

    def test_update_user_streak_first_time(self):
        """Test streak update logic for first-time check-in."""
        user = User(username="streakuser", email="streak@gamil.com")
        today = date.today()

        is_comeback, streak = update_user_streak(user, today)

        assert is_comeback == False
        assert streak == 1

    def test_update_user_streak_consecutive(self):
        """Test streak update logic for consecutive check-ins."""
        user = User(username="consecutiveuser", email="consecutive@gamil.com")
        user.current_streak = 6
        user.last_check_in_date = date.today() - timedelta(days=1)  # Yesterday

        today = date.today()

        is_comeback, streak = update_user_streak(user, today)

        assert is_comeback == False
        assert streak == 7

    def test_update_user_streak_reset_after_break(self):
        """Test streak reset after a break."""
        user = User(username="resetuser", email="reset@gamil.com")
        user.current_streak = 10
        user.last_check_in_date = date.today() - timedelta(days=3)  # 3 days ago

        today = date.today()

        is_comeback, streak = update_user_streak(user, today)

        assert is_comeback == True
        assert streak == 1


class TestMilestoneBonus:

    def test_milestone_bonus(self):
        """Test milestone bonus calculation."""
        # Test for various streaks
        assert calculate_milestone_bonus(1) == 0
        assert calculate_milestone_bonus(5) == 0

        assert calculate_milestone_bonus(7) == 50
        assert calculate_milestone_bonus(14) == 50

        assert calculate_milestone_bonus(30) == 200
        assert calculate_milestone_bonus(60) == 200

        assert calculate_milestone_bonus(100) == 500
        assert calculate_milestone_bonus(200) == 500
