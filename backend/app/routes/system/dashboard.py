from pydantic import BaseModel
from typing import List
from datetime import date, timedelta
from random import randint, uniform
from fastapi import APIRouter, Depends


class WeeklyIncomePoint(BaseModel):
    date: date
    amount: float

class ClientStatusCount(BaseModel):
    total: int
    paid: int
    unpaid: int
    in_progress: int
    added_today: int

class DashboardDataSchema(BaseModel):
    weekly_income: List[WeeklyIncomePoint]
    total_income: float
    monthly_income: float
    client_stats: ClientStatusCount


def get_fake_data() -> DashboardDataSchema:
    today = date.today()
    weekly_income = [
        WeeklyIncomePoint(
            date=today - timedelta(days=i),
            amount=round(uniform(200, 1200), 2)
        )
        for i in range(6, -1, -1)
    ]

    return DashboardDataSchema(
        weekly_income=weekly_income,
        total_income=sum(p.amount for p in weekly_income) + 32000,
        monthly_income=round(uniform(7000, 15000), 2),
        client_stats=ClientStatusCount(
            total=randint(200, 500),
            paid=randint(80, 200),
            unpaid=randint(20, 100),
            in_progress=randint(30, 100),
            added_today=randint(1, 10),
        )
    )

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardDataSchema)
async def get_dashboard():
    return get_fake_data()

