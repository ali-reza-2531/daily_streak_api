from datetime import date
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_utils import engine, get_db, Base
from models import User, CheckIn
from schemas import UserCreate, UserResponse, CheckInRequest, CheckInResponse
from motivational import get_motivational_message
import os
from fastapi.middleware.cors import CORSMiddleware


# Create the database tables
Base.metadata.create_all(bind=engine)
# main.py - Add environment handling

app = FastAPI(
    title="Daily Streak API",
    description="A gamified daily check-in system",
    version="1.0.0"
)

# Add CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database URL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")


@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Daily Streak API is running!"}


@app.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """ Get all users."""
    users = db.query(User).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """ Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """ Create a new user."""

    try:
        # Check if username already exists
        existing_username = db.query(User).filter(
            User.username == user.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Create new user
        db_user = User(username=user.username, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except HTTPException:
        # Re-raise HTTP exceptions (like our 400 errors)
        db.rollback()
        raise

    except Exception as e:
        # Only catch non-HTTP exceptions
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {e}")


@app.post('/checkin/', response_model=CheckInResponse)
def check_in(checkin_request: CheckInRequest, db: Session = Depends(get_db)):
    """ Handle user check-in and update streaks."""
    try:
        # Validate user exists
        user = db.query(User).filter(
            User.id == checkin_request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        today = date.today()
        if user.last_check_in_date == today:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="You have already checked in today. Keep up the great streak!")

        # update user streak
        is_comeback, user.current_streak = update_user_streak(
            user=user, today=today)

        # calculate milestone bonus
        milestone_bonus = calculate_milestone_bonus(streak=user.current_streak)

        # Calculate XP earned
        xp_earned = 10 + milestone_bonus
        user.total_xp += xp_earned
        user.last_check_in_date = today
        checkin = CheckIn(
            user_id=user.id, xp_earned=xp_earned, checkin_date=today)
        db.add(checkin)
        db.commit()
        db.refresh(user)
        db.refresh(checkin)

        # Return response
        return CheckInResponse(
            success=True,
            message=get_motivational_message(
                user.current_streak, is_comeback=is_comeback),
            xp_earned=xp_earned,
            current_streak=user.current_streak,
            total_xp=user.total_xp,
            milestone_bonus=milestone_bonus
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like our 400 errors)
        db.rollback()
        raise
    except Exception as e:
        # Only catch non-HTTP exceptions
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check in: {e}")


@app.get("/leaderboard/", response_model=List[UserResponse])
def get_leaderboard(db: Session = Depends(get_db)):
    """ Get the leaderboard of top 10 users by total XP."""

    users = db.query(User).order_by(User.total_xp.desc()).limit(10).all()
    return users


def update_user_streak(user: User, today: date) -> tuple[bool, int]:
    """
    Update the user streak 

    Args:
        user (User): The user object to update.
        today (date): The current date.

    Returns:
        tuple: (is_comeback (bool): Whether the user is making a comeback,
                current_streak (int): The current streak count.
            )
    """
    is_comeback = False

    if user.last_check_in_date is None:
        user.current_streak = 1

    elif user.last_check_in_date == today.replace(day=today.day - 1):
        user.current_streak += 1

    else:
        user.current_streak = 1
        is_comeback = True

    return is_comeback, user.current_streak


def calculate_milestone_bonus(streak: int) -> int:
    """
    Calculate bonus XP based on streak milestones.

    Args:
        streak (int): The current streak count.

    Returns:
        int: Bonus XP for the current streak.
    """
    if streak % 100 == 0:
        return 500
    elif streak % 30 == 0:
        return 200
    elif streak % 7 == 0:
        return 50
    return 0


app = app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
