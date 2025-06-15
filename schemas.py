from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import date

from fastapi import FastAPI

app = FastAPI()


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50,
                          description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")


class CheckInRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user checking in")


class UserResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    username: str = Field(..., min_length=2, max_length=50,
                          description="Username of the user")
    email: str = Field(..., description="Email address of the user")
    total_xp: int = Field(..., ge=0, description="Total XP earned by the user")
    current_streak: int = Field(...,
                                description="Current streak of consecutive check-ins")
    last_checkin_date: Optional[date] = Field(
        None, description="Date of the last check-in by the user"
    )


class CheckInResponse(BaseModel):
    success: bool = Field(...,
                          description="Indicates if the check-in was successful")
    message: str = Field(
        ..., description="Message providing additional information about the check-in")
    xp_earned: int = Field(..., ge=0,
                           description="XP earned from the check-in")
    current_streak: int = Field(...,
                                description="Current streak of consecutive check-ins")
    total_xp: int = Field(..., ge=0, description="Total XP after the check-in")
    milestone_bonus: int = Field(
        0, ge=0, description="Bonus XP earned for reaching a milestone (if applicable)"
    )


class LeaderboardEntry(BaseModel):
    rank: int = Field(..., ge=1,
                      description="Rank of the user in the leaderboard")
    username: str = Field(..., min_length=2, max_length=50,
                          description="Username of the user")
    total_xp: int = Field(..., ge=0, description="Total XP earned by the user")
    current_streak: int = Field(...,
                                description="Current streak of consecutive check-ins")
