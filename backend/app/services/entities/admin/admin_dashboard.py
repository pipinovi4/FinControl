from __future__ import annotations

import re
from datetime import datetime, UTC, timedelta, date
from typing import Sequence, Any, Mapping, Optional, Tuple
from uuid import UUID

from sqlalchemy import (
    select, func, extract, update, and_, or_, literal_column, exists
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.routes.entities.crud.dashboard.types import DeletedFilter
from app.models.entities.application import Application
from app.models.entities.credit import Credit, CreditStatus
from app.models.entities.user import User
from app.models.entities.worker import Worker
from app.models.entities.broker import Broker
from app.utils.decorators import handle_exceptions

from app.schemas.entities.application_schema import (
    ApplicationAdminOut,
    WorkerApplicationNewToday,
    BrokerApplicationNewToday,
    ApplicationNewToday,
)
from app.schemas.entities.worker_schema import WorkerAdminOut
from app.schemas.entities.broker_schema import BrokerAdminOut
from app.schemas.entities.promotion_schema import (
    PromotionCreate,
    PromotionUpdate,
    PromotionSummaryOut,
    TopWorkerOut,
)
from app.models.entities.promotion import Promotion, PromotionEnum
from app.services.entities import WorkerService, BrokerService


class AdminDashboard:
    """
    NEW version — Application-centric system.
    Everything now works on:
        Application + Credit + User(Worker/Broker)
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ─────────────────────────────
    # 📊 GLOBAL AGGREGATES (OK)
    # ─────────────────────────────

    @handle_exceptions()
    async def get_total_sum_credits(self) -> float:
        stmt = select(func.coalesce(func.sum(Credit.amount), 0.0))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_month_sum_credits(self) -> float:
        now = datetime.now(UTC)
        stmt = (
            select(func.coalesce(func.sum(Credit.amount), 0.0))
            .where(
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_users(self) -> int:
        stmt = select(func.count(User.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_applications(self) -> int:
        stmt = select(func.count(Application.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_brokers(self) -> int:
        stmt = select(func.count(Broker.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_workers(self) -> int:
        stmt = select(func.count(Worker.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_credits(self) -> int:
        stmt = select(func.count(Credit.id))
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 📅 DATE RANGE
    # ─────────────────────────────

    @handle_exceptions()
    async def get_sum_credits_by_date(self, date_from: date, date_to: date) -> float:
        stmt = (
            select(func.coalesce(func.sum(Credit.amount), 0.0))
            .where(Credit.issued_at.between(date_from, date_to))
        )
        return (await self.db.execute(stmt)).scalar_one()
    # ─────────────────────────────
    # 👷 WORKER NEW TODAY/YESTERDAY (Applications)
    # ─────────────────────────────

    @handle_exceptions()
    async def get_today_new_applications_worker(self) -> list[WorkerApplicationNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(Application).where(Application.taken_at_worker >= today_start)
        apps = (await self.db.execute(stmt)).scalars().all()
        return [WorkerApplicationNewToday(id=a.id, taken_at_worker=a.taken_at_worker) for a in apps]

    @handle_exceptions()
    async def get_yesterday_new_applications_worker(self) -> list[WorkerApplicationNewToday]:
        now = datetime.utcnow()
        y_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        y_end = y_start + timedelta(days=1)

        stmt = (
            select(Application)
            .where(Application.taken_at_worker >= y_start, Application.taken_at_worker < y_end)
        )
        apps = (await self.db.execute(stmt)).scalars().all()
        return [WorkerApplicationNewToday(id=a.id, taken_at_worker=a.taken_at_worker) for a in apps]

    # ─────────────────────────────
    # 🧑‍💼 BROKER NEW TODAY/YESTERDAY
    # ─────────────────────────────

    @handle_exceptions()
    async def get_today_new_applications_broker(self) -> list[BrokerApplicationNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = select(Application).where(Application.taken_at_broker >= today_start)
        apps = (await self.db.execute(stmt)).scalars().all()
        return [BrokerApplicationNewToday(id=a.id, taken_at_broker=a.taken_at_broker) for a in apps]

    @handle_exceptions()
    async def get_yesterday_new_applications_broker(self) -> list[BrokerApplicationNewToday]:
        now = datetime.utcnow()
        y_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        y_end = y_start + timedelta(days=1)

        stmt = (
            select(Application)
            .where(Application.taken_at_broker >= y_start, Application.taken_at_broker < y_end)
        )
        apps = (await self.db.execute(stmt)).scalars().all()
        return [BrokerApplicationNewToday(id=a.id, taken_at_broker=a.taken_at_broker) for a in apps]

    # ─────────────────────────────
    # 👨‍💻 NEW WORKERS / BROKERS
    # ─────────────────────────────

    @handle_exceptions()
    async def get_today_new_workers(self) -> list[ApplicationNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(Worker).where(Worker.created_at >= today_start)
        workers = (await self.db.execute(stmt)).scalars().all()
        return [ApplicationNewToday(id=w.id, created_at=w.created_at) for w in workers]

    @handle_exceptions()
    async def get_yesterday_new_workers(self) -> list[ApplicationNewToday]:
        now = datetime.utcnow()
        y_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        y_end = y_start + timedelta(days=1)

        stmt = select(Worker).where(Worker.created_at >= y_start, Worker.created_at < y_end)
        workers = (await self.db.execute(stmt)).scalars().all()
        return [ApplicationNewToday(id=w.id, created_at=w.created_at) for w in workers]

    @handle_exceptions()
    async def get_today_new_brokers(self) -> list[ApplicationNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(Broker).where(Broker.created_at >= today_start)
        brokers = (await self.db.execute(stmt)).scalars().all()
        return [ApplicationNewToday(id=b.id, created_at=b.created_at) for b in brokers]

    @handle_exceptions()
    async def get_yesterday_new_brokers(self) -> list[ApplicationNewToday]:
        now = datetime.utcnow()
        y_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        y_end = y_start + timedelta(days=1)

        stmt = select(Broker).where(Broker.created_at >= y_start, Broker.created_at < y_end)
        brokers = (await self.db.execute(stmt)).scalars().all()
        return [ApplicationNewToday(id=b.id, created_at=b.created_at) for b in brokers]

    # ─────────────────────────────
    # 🔎 JSONB SEARCH (по Application.data)
    # ─────────────────────────────

    @staticmethod
    def _applications_search_clause(search: str):
        if not search:
            return None

        terms = [t.strip() for t in re.split(r"[\s,]+", search) if t.strip()]
        if not terms:
            return None

        and_groups = []
        for t in terms:
            like = f"%{t}%"

            disj = [
                Application.data["full_name"].astext.ilike(like),
                Application.data["email"].astext.ilike(like),
                Application.data["phone_number"].astext.ilike(like),
            ]

            try:
                uid = UUID(t)
                disj.append(Application.id == uid)
            except Exception:
                pass

            and_groups.append(or_(*disj))

        return and_(*and_groups)

    # ─────────────────────────────
    # 📦 BUCKET APPLICATIONS
    # ─────────────────────────────

    @handle_exceptions()
    async def get_bucket_applications(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        deleted: DeletedFilter = "all",
    ) -> Tuple[list[ApplicationAdminOut], int]:

        where_clause = self._applications_search_clause(search)

        # deleted filter
        if deleted == "active":
            deleted_clause = Application.is_deleted.is_(False)
        elif deleted == "only":
            deleted_clause = Application.is_deleted.is_(True)
        else:
            deleted_clause = None

        final = where_clause
        if deleted_clause:
            final = and_(final, deleted_clause) if final else deleted_clause

        # Count
        count_stmt = select(func.count()).select_from(Application)
        if final:
            count_stmt = count_stmt.where(final)
        total = (await self.db.execute(count_stmt)).scalar_one()

        # Data
        stmt = (
            select(Application)
            .where(final) if final else select(Application)
        )
        stmt = (
            stmt
            .options(
                selectinload(Application.worker),
                selectinload(Application.broker),
                selectinload(Application.credits),
            )
            .order_by(Application.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        apps = (await self.db.execute(stmt)).scalars().all()
        return [ApplicationAdminOut.model_validate(a) for a in apps], total

    # ─────────────────────────────
    # SINGLE ENTITY FETCH
    # ─────────────────────────────

    @handle_exceptions()
    async def get_application(self, app_id: UUID) -> ApplicationAdminOut:
        stmt = (
            select(Application)
            .where(Application.id == app_id)
            .options(
                selectinload(Application.worker),
                selectinload(Application.broker),
                selectinload(Application.credits),
            )
        )
        app = (await self.db.execute(stmt)).scalar_one_or_none()
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        return ApplicationAdminOut.model_validate(app)

    @handle_exceptions()
    async def get_worker(self, worker_id: UUID):
        stmt = (
            select(Worker)
            .where(Worker.id == worker_id)
            .options(selectinload(Worker.applications))
        )
        worker = (await self.db.execute(stmt)).scalar_one_or_none()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        return WorkerAdminOut.model_validate(worker)

    @handle_exceptions()
    async def get_broker(self, broker_id: UUID):
        stmt = (
            select(Broker)
            .where(Broker.id == broker_id)
            .options(selectinload(Broker.applications))
        )
        broker = (await self.db.execute(stmt)).scalar_one_or_none()
        if not broker:
            raise HTTPException(status_code=404, detail="Broker not found")
        return BrokerAdminOut.model_validate(broker)

    # ─────────────────────────────
    # USER DELETE / RESTORE
    # ─────────────────────────────

    @handle_exceptions()
    async def delete_user(self, user_id: UUID) -> None:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_deleted=True, deleted_at=datetime.utcnow())
        )
        await self.db.commit()

    @handle_exceptions()
    async def restore_user(self, user_id: UUID, *, reactivate: bool = False) -> None:
        values = {"is_deleted": False, "deleted_at": None}
        if reactivate:
            values["is_active"] = True

        await self.db.execute(
            update(User).where(User.id == user_id).values(**values)
        )
        await self.db.commit()

    # ─────────────────────────────
    # REASSIGNMENTS
    # ─────────────────────────────

    @handle_exceptions()
    async def worker_reassign_applications_by_email(self, app_id: UUID, worker_email: str | None):
        new_worker_id = None
        if worker_email:
            worker = await WorkerService(self.db).get_by_email(worker_email)
            if not worker:
                raise HTTPException(404, "Worker not found")
            new_worker_id = worker.id

        await self.db.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(
                worker_id=new_worker_id,
                taken_at_worker=datetime.utcnow() if new_worker_id else None,
            )
        )
        await self.db.commit()

    @handle_exceptions()
    async def broker_reassign_application_by_email(self, app_id: UUID, broker_email: str | None):
        new_broker_id = None
        if broker_email:
            broker = await BrokerService(self.db).get_by_email(broker_email)
            if not broker:
                raise HTTPException(404, "Broker not found")
            new_broker_id = broker.id

        await self.db.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(
                broker_id=new_broker_id,
                taken_at_broker=datetime.utcnow() if new_broker_id else None,
            )
        )
        await self.db.commit()
    # ─────────────────────────────
    # 📈 CREDIT STATS — COUNT ACTIVE, COMPLETED
    # ─────────────────────────────

    @handle_exceptions()
    async def get_count_active_credits(self) -> int:
        stmt = (
            select(func.count(Credit.id))
            .where(
                Credit.status != CreditStatus.COMPLETED,
                Credit.is_deleted.is_(False),
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_completed_credits(self) -> int:
        stmt = (
            select(func.count(Credit.id))
            .where(
                Credit.status == CreditStatus.COMPLETED,
                Credit.is_deleted.is_(False),
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 📅 MONTHLY & YEARLY SUMMARIES (Application-based)
    # ─────────────────────────────

    def _dialect(self) -> str:
        return (self.db.bind and self.db.bind.dialect.name) or "postgresql"

    @handle_exceptions()
    async def get_credits_for_month(self, month: str) -> list[dict[str, Any]]:
        """
        month example: "2025-03"
        Returns list: [{date, amount}]
        """

        try:
            year, m = map(int, month.split("-"))
            start_date = date(year, m, 1)
            end_date = date(year + (1 if m == 12 else 0),
                            1 if m == 12 else m + 1,
                            1)
        except Exception:
            raise ValueError("Invalid month format. Expected YYYY-MM")

        # Day-key differs for sqlite
        if self._dialect() == "sqlite":
            day_key = func.strftime("%Y-%m-%d", Credit.issued_at)
        else:
            day_key = func.date(Credit.issued_at)

        stmt = (
            select(
                day_key.label("day"),
                func.coalesce(func.sum(Credit.amount), 0.0).label("total")
            )
            .where(
                Credit.is_deleted.is_(False),
                Credit.issued_at >= start_date,
                Credit.issued_at < end_date,
            )
            .group_by(day_key)
            .order_by(day_key)
        )

        rows = (await self.db.execute(stmt)).all()

        totals = {}
        for day_value, total in rows:
            d = date.fromisoformat(day_value) if isinstance(day_value, str) else day_value
            totals[d] = float(total)

        # fill all days
        out = []
        for i in range((end_date - start_date).days):
            cur = start_date + timedelta(days=i)
            out.append({"date": cur.isoformat(), "amount": round(totals.get(cur, 0.0), 2)})
        return out

    @handle_exceptions()
    async def get_credits_for_year(self, year: int) -> list[dict[str, Any]]:
        """
        Returns: list of 12 items:
            [{"month": "01", "amount": ...}, ...]
        """

        if self._dialect() == "sqlite":
            month_key = func.cast(func.strftime("%m", Credit.issued_at), int)
            year_cond = func.strftime("%Y", Credit.issued_at) == str(year)
        else:
            month_key = extract("month", Credit.issued_at)
            year_cond = extract("year", Credit.issued_at) == year

        stmt = (
            select(
                month_key.label("month"),
                func.coalesce(func.sum(Credit.amount), 0.0).label("total")
            )
            .where(
                Credit.is_deleted.is_(False),
                year_cond,
            )
            .group_by(month_key)
            .order_by(month_key)
        )

        rows = (await self.db.execute(stmt)).all()

        totals = {int(m): float(total) for m, total in rows}

        out = []
        for m in range(1, 12 + 1):
            out.append({
                "month": f"{m:02d}",
                "amount": round(totals.get(m, 0.0), 2),
            })
        return out

    # ─────────────────────────────
    # 🏆 TOP WORKERS BY CREDIT COUNT
    # ─────────────────────────────

    @handle_exceptions()
    async def top_workers_by_count(self, *, limit: int = 3) -> list[TopWorkerOut]:
        stmt = (
            select(
                Credit.worker_id.label("worker_id"),
                Worker.username.label("username"),
                func.count(Credit.id).label("credits_count"),
            )
            .join(Worker, Worker.id == Credit.worker_id)
            .where(
                Credit.worker_id.isnot(None),
                Credit.is_deleted.is_(False)
            )
            .group_by(Credit.worker_id, Worker.username)
            .order_by(func.count(Credit.id).desc())
            .limit(limit)
        )

        rows = (await self.db.execute(stmt)).all()

        return [
            TopWorkerOut(
                worker_id=row.worker_id,
                username=row.username,
                credits_count=int(row.credits_count),
            )
            for row in rows
        ]

    # ─────────────────────────────
    # 🎯 PROMOTIONS — CRUD & SUMMARY
    # ─────────────────────────────

    @handle_exceptions()
    async def create_promotion(self, payload: PromotionCreate) -> Promotion:
        promo = Promotion(**payload.model_dump())
        self.db.add(promo)
        await self.db.commit()
        await self.db.refresh(promo)
        return promo

    @handle_exceptions()
    async def update_promotion(self, promo_id: UUID, payload: PromotionUpdate) -> Promotion:
        promo = await self.db.get(Promotion, promo_id)
        if not promo:
            raise HTTPException(404, "Promotion not found")

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(promo, k, v)

        await self.db.commit()
        await self.db.refresh(promo)
        return promo

    @handle_exceptions()
    async def deactivate_promotion(self, promo_id: UUID) -> None:
        promo = await self.db.get(Promotion, promo_id)
        if not promo:
            raise HTTPException(404, "Promotion not found")

        promo.is_active = False
        await self.db.commit()

    @handle_exceptions()
    async def activate_promotion(self, promo_id: UUID, *, deactivate_others_same_type: bool = False) -> Promotion:
        promo = await self.db.get(Promotion, promo_id)
        if not promo:
            raise HTTPException(404, "Promotion not found")

        if deactivate_others_same_type:
            await self.db.execute(
                update(Promotion)
                .where(
                    Promotion.id != promo_id,
                    Promotion.promotion_type == promo.promotion_type,
                    Promotion.is_active.is_(True),
                )
                .values(is_active=False)
            )

        promo.is_active = True
        await self.db.commit()
        await self.db.refresh(promo)
        return promo

    @handle_exceptions()
    async def list_promotions(self, *, is_active: bool | None = None,
                              ptype: PromotionEnum | None = None,
                              limit: int = 50) -> list[Promotion]:
        stmt = (
            select(Promotion)
            .order_by(Promotion.created_at.desc())
            .limit(limit)
        )
        if is_active is not None:
            stmt = stmt.where(Promotion.is_active.is_(is_active))
        if ptype is not None:
            stmt = stmt.where(Promotion.promotion_type == ptype)

        return list((await self.db.execute(stmt)).scalars().all())

    @handle_exceptions()
    async def list_promotions_summary(self, *, ptype: PromotionEnum | None = None,
                                      limit: int = 12) -> list[PromotionSummaryOut]:
        promos = await self.list_promotions(is_active=True, ptype=ptype, limit=limit)
        return [
            PromotionSummaryOut(
                id=p.id,
                promotion_type=p.promotion_type,
                is_active=p.is_active,
                created_at=p.created_at,
                description=p.description,
            )
            for p in promos
        ]

    @handle_exceptions()
    async def get_promotion(self, promo_id: UUID) -> Promotion:
        promo = await self.db.get(Promotion, promo_id)
        if not promo:
            raise HTTPException(404, "Promotion not found")
        return promo

    # ─────────────────────────────
    # 📦 BUCKET — WORKERS (with filters)
    # ─────────────────────────────

    @handle_exceptions()
    async def filter_bucket_workers(
        self,
        skip: int = 0,
        limit: int = 6,
        *,
        email: str | None = None,
        username: str | None = None,
        is_deleted: bool | None = None,
    ) -> tuple[list[WorkerAdminOut], int]:
        conditions = []

        if email:
            conditions.append(Worker.email.ilike(f"%{email}%"))
        if username:
            conditions.append(Worker.username.ilike(f"%{username}%"))
        if is_deleted is not None:
            conditions.append(Worker.is_deleted.is_(is_deleted))

        where_clause = and_(*conditions) if conditions else True

        # count
        total = (await self.db.execute(
            select(func.count()).select_from(Worker).where(where_clause)
        )).scalar_one()

        # data
        stmt = (
            select(Worker)
            .where(where_clause)
            .order_by(Worker.username.asc())
            .offset(skip)
            .limit(limit)
        )

        workers = (await self.db.execute(stmt)).scalars().all()
        return [WorkerAdminOut.model_validate(w) for w in workers], total

    # ─────────────────────────────
    # 📦 BUCKET — BROKERS (with filters)
    # ─────────────────────────────

    @handle_exceptions()
    async def filter_bucket_brokers(
        self,
        skip: int = 0,
        limit: int = 6,
        *,
        email: str | None = None,
        company_name: str | None = None,
        region: str | None = None,
        is_deleted: bool | None = None,
    ) -> tuple[list[BrokerAdminOut], int]:

        conditions = []

        if email:
            conditions.append(Broker.email.ilike(f"%{email}%"))
        if company_name:
            conditions.append(Broker.company_name.ilike(f"%{company_name}%"))

        if region:
            # region is ARRAY(String)
            subq = select(literal_column("1")).where(
                literal_column("region_item").ilike(f"%{region}%")
            ).select_from(func.unnest(Broker.region).alias("region_item"))
            conditions.append(exists(subq))

        if is_deleted is not None:
            conditions.append(Broker.is_deleted.is_(is_deleted))

        where_clause = and_(*conditions) if conditions else True

        # count
        total = (await self.db.execute(
            select(func.count()).select_from(Broker).where(where_clause)
        )).scalar_one()

        stmt = (
            select(Broker)
            .where(where_clause)
            .order_by(Broker.company_name.asc())
            .offset(skip)
            .limit(limit)
        )

        brokers = (await self.db.execute(stmt)).scalars().all()

        return [BrokerAdminOut.model_validate(b) for b in brokers], total

    # ─────────────────────────────
    # 🔧 EDIT USER + APPLICATION / BROKER / WORKER
    # ─────────────────────────────

    async def _edit_user_and_entity(self, model, entity_id: UUID, fields: Mapping[str, Any]) -> None:
        """
        Generic updater that edits User table + model table (Application/Broker/Worker).
        """
        if not fields:
            return

        # user fields (email, is_active)
        user_fields = {}
        for key in ("email", "is_active"):
            if key in fields:
                user_fields[key] = fields[key]

        model_fields = dict(fields)
        for k in user_fields:
            model_fields.pop(k, None)

        # Update User
        if user_fields:
            await self.db.execute(
                update(User)
                .where(User.id == entity_id)
                .values(**user_fields)
            )

        # Update model (Application / Broker / Worker)
        if model_fields:
            await self.db.execute(
                update(model)
                .where(model.id == entity_id)
                .values(**model_fields)
            )

        await self.db.commit()

    @handle_exceptions()
    async def edit_application_data(self, app_id: UUID, fields: Mapping[str, Any]) -> None:
        await self._edit_user_and_entity(Application, app_id, fields)

    @handle_exceptions()
    async def edit_broker_data(self, broker_id: UUID, fields: Mapping[str, Any]) -> None:
        await self._edit_user_and_entity(Broker, broker_id, fields)

    @handle_exceptions()
    async def edit_worker_data(self, worker_id: UUID, fields: Mapping[str, Any]) -> None:
        await self._edit_user_and_entity(Worker, worker_id, fields)
    # ─────────────────────────────
    # 🔧 CREDIT CONTROL
    # ─────────────────────────────

    @handle_exceptions()
    async def force_complete_credit(self, credit_id: UUID) -> None:
        """
        Mark credit fully paid + set completed.
        """
        await self.db.execute(
            update(Credit)
            .where(Credit.id == credit_id)
            .values(
                paid_amount=Credit.total_amount,
                status=CreditStatus.COMPLETED,
                last_payment_at=datetime.now(UTC),
            )
        )
        await self.db.commit()

    @handle_exceptions()
    async def change_credit_status(self, credit_id: UUID, new_status: str) -> None:
        """
        Direct status override.
        """
        await self.db.execute(
            update(Credit)
            .where(Credit.id == credit_id)
            .values(status=new_status)
        )
        await self.db.commit()
    # ─────────────────────────────
    # 📊 SIGNED / UNSIGNED APPLICATIONS
    # ─────────────────────────────

    @handle_exceptions()
    async def get_count_signed_applications_by_worker(self, worker_id: UUID) -> int:
        stmt = select(func.count(Application.id)).where(
            Application.worker_id == worker_id
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_unsigned_applications(self) -> int:
        stmt = select(func.count(Application.id)).where(
            Application.worker_id.is_(None)
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_total_count_signed_applications(self) -> int:
        stmt = select(func.count(Application.id)).where(
            Application.worker_id.isnot(None)
        )
        return (await self.db.execute(stmt)).scalar_one()
    # ─────────────────────────────
    # 📦 UNIVERSAL PAGINATION
    # ─────────────────────────────

    async def _paginate_with_total(
        self,
        model,
        *,
        skip: int = 0,
        limit: int = 20,
        where_clause=None,
        options: tuple = (),
        order_by=None,
        deleted: DeletedFilter = "all",
    ) -> Tuple[list, int]:

        # deleted filter
        if deleted == "active":
            deleted_clause = model.is_deleted.is_(False)
        elif deleted == "only":
            deleted_clause = model.is_deleted.is_(True)
        else:
            deleted_clause = None

        if deleted_clause is not None:
            final_where = and_(where_clause, deleted_clause) if where_clause else deleted_clause
        else:
            final_where = where_clause

        # Count
        stmt_count = select(func.count()).select_from(model)
        if final_where is not None:
            stmt_count = stmt_count.where(final_where)
        total = (await self.db.execute(stmt_count)).scalar_one()

        # Data
        stmt = select(model)
        if final_where is not None:
            stmt = stmt.where(final_where)

        stmt = stmt.order_by(order_by or model.created_at.desc())
        stmt = stmt.offset(skip).limit(limit)

        if options:
            stmt = stmt.options(*options)

        rows = (await self.db.execute(stmt)).scalars().all()
        return rows, total

    @staticmethod
    def _applications_search_clause(search: str):
        if not search:
            return None

        terms = [t.strip() for t in re.split(r"[\s,]+", search) if t.strip()]
        if not terms:
            return None

        and_groups = []

        for t in terms:
            like = f"%{t}%"

            disj = [
                Application.data["full_name"].astext.ilike(like),
                Application.data["email"].astext.ilike(like),
                Application.data["phone_number"].astext.ilike(like),
                Application.data["address"].astext.ilike(like),
            ]

            # normalized phone
            disj.append(
                func.replace(Application.data["phone_number"].astext, '-', '').ilike(
                    f"%{t.replace('-', '')}%"
                )
            )

            # UUID exact match
            try:
                uid = UUID(t)
                disj.append(Application.id == uid)
            except Exception:
                pass

            and_groups.append(or_(*disj))

        return and_(*and_groups)
