from __future__ import annotations

import re

from datetime import datetime, UTC, timedelta, date
from typing import Sequence, Any, Mapping, Optional, Tuple

from sqlalchemy import (
    select,
    func,
    extract,
    update,
    and_,
    literal_column,
    exists,
    or_,
)
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.routes.entities.crud.dashboard.admin_dashboard_router import DeletedFilter
from app.models import Client, Broker, Worker, User
from app.models.entities.credit import Credit, CreditStatus
from app.schemas.entities.broker_schema import BrokerAdminOut
from app.schemas.entities.client_schema import WorkerClientNewToday, UserNewToday, ClientAdminOut, ClientBrokerOut
from app.schemas.entities.worker_schema import WorkerAdminOut
from app.services.entities import WorkerService, BrokerService
from app.utils.decorators import handle_exceptions
from app.models.entities.promotion import Promotion, PromotionEnum
from app.schemas.entities.promotion_schema import (
    PromotionCreate, PromotionUpdate, PromotionSummaryOut, TopWorkerOut
)


class AdminDashboard:
    """
    High-level service for global analytics & administration.
    Works on *all* users, credits.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ─────────────────────────────
    # 📊 GLOBAL AGGREGATES
    # ─────────────────────────────

    @handle_exceptions()
    async def get_total_sum_credits(self) -> int:
        stmt = select(func.coalesce(func.sum(Credit.amount), 0))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_month_sum_credits(self) -> int:
        now = datetime.now(UTC)
        stmt = (
            select(func.coalesce(func.sum(Credit.amount), 0))
            .where(
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_users(self) -> int:
        # общее кол-во пользователей (включая удалённых)
        stmt = select(func.count(User.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_clients(self) -> int:
        stmt = select(func.count(Client.id))
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
    # 📅 DATE-RANGE AGGREGATES
    # ─────────────────────────────

    @handle_exceptions()
    async def get_sum_credits_by_date(
        self, date_from: date, date_to: date
    ) -> int:
        stmt = (
            select(func.coalesce(func.sum(Credit.total_amount), 0))
            .where(Credit.issued_at.between(date_from, date_to))
        )
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 🔎 TODAY / PER-WORKER
    # ─────────────────────────────

    @handle_exceptions()
    async def get_worker_sum_today_new_clients(self, worker_id: UUID) -> int:
        start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(func.count())
            .select_from(Client)
            .where(Client.worker_id == worker_id, Client.taken_at_worker >= start)
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_today_new_clients_worker(self) -> list[WorkerClientNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = select(Client).where(Client.taken_at_worker >= today_start)
        result = await self.db.execute(stmt)
        return [WorkerClientNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_yesterday_new_clients_worker(self) -> list[WorkerClientNewToday]:
        now = datetime.utcnow()
        yesterday_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_end = yesterday_start + timedelta(days=1)

        stmt = (
            select(Client)
            .where(
                Client.taken_at_broker >= yesterday_start,
                Client.taken_at_broker < yesterday_end,
            )
        )
        result = await self.db.execute(stmt)
        return [WorkerClientNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_today_new_clients_broker(self) -> list[WorkerClientNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = select(Client).where(Client.taken_at_broker >= today_start)
        result = await self.db.execute(stmt)
        rows = (r for r in result.scalars() if r.taken_at_worker)
        return [WorkerClientNewToday.model_validate(r) for r in rows]

    @handle_exceptions()
    async def get_yesterday_new_clients_broker(self) -> list[WorkerClientNewToday]:
        now = datetime.utcnow()
        yesterday_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_end = yesterday_start + timedelta(days=1)

        stmt = (
            select(Client)
            .where(
                Client.taken_at_broker >= yesterday_start,
                Client.taken_at_broker < yesterday_end,
            )
        )
        result = await self.db.execute(stmt)
        return [WorkerClientNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_today_new_workers(self) -> list[UserNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(Worker).where(Worker.created_at >= today_start)
        result = await self.db.execute(stmt)
        return [UserNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_yesterday_new_workers(self) -> list[UserNewToday]:
        now = datetime.utcnow()
        yesterday_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_end = yesterday_start + timedelta(days=1)

        stmt = select(Worker).where(Worker.created_at >= yesterday_start, Worker.created_at < yesterday_end)
        result = await self.db.execute(stmt)
        return [UserNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_today_new_brokers(self) -> list[UserNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(Broker).where(Broker.created_at >= today_start)
        result = await self.db.execute(stmt)
        return [UserNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_yesterday_new_brokers(self) -> list[UserNewToday]:
        now = datetime.utcnow()
        yesterday_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_end = yesterday_start + timedelta(days=1)

        stmt = select(Broker).where(Broker.created_at >= yesterday_start, Broker.created_at < yesterday_end)
        result = await self.db.execute(stmt)
        return [UserNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_count_signed_clients_by_worker(self, worker_id: UUID) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id == worker_id)
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_unsigned_clients_by_worker(self) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id.is_(None))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_total_count_signed_clients_by_brokers(self) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id.isnot(None))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_total_count_unsigned_clients_by_brokers(self) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id.is_(None))
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 📦 BUCKET (PAGINATION) + filters
    # ─────────────────────────────

    async def _paginate_with_total(
            self,
            model,
            *,
            skip: int = 0,
            limit: int = 20,
            where_clause: Any = None,
            options: tuple = (),
            order_by=None,
            deleted: DeletedFilter = "all",  # ⟵ нове
    ) -> Tuple[list, int]:
        """Generic pagination with COUNT(*) using the same WHERE."""
        # apply deleted filter
        if deleted == "active":
            deleted_clause = model.is_deleted.is_(False)
        elif deleted == "only":
            deleted_clause = model.is_deleted.is_(True)
        else:
            deleted_clause = None

        final_where = where_clause
        if deleted_clause is not None:
            final_where = and_(where_clause, deleted_clause) if where_clause is not None else deleted_clause

        count_stmt = select(func.count()).select_from(model)
        if final_where is not None:
            count_stmt = count_stmt.where(final_where)
        total = int((await self.db.execute(count_stmt)).scalar_one())

        data_stmt = select(model)
        if final_where is not None:
            data_stmt = data_stmt.where(final_where)
        if order_by is None:
            order_by = model.created_at.desc()
        data_stmt = data_stmt.order_by(order_by).offset(skip).limit(limit)
        if options:
            data_stmt = data_stmt.options(*options)

        rows = (await self.db.execute(data_stmt)).scalars().all()
        return rows, total

    # ---------- search builder for clients ----------
    @staticmethod
    def _clients_search_clause(search: str):
        if not search:
            return None
        terms = [t.strip() for t in re.split(r"[\s,]+", search) if t.strip()]
        if not terms:
            return None

        phone_norm = func.regexp_replace(Client.phone_number, r'[^0-9]', '', 'g')
        and_groups = []
        for t in terms:
            like = f"%{t}%"
            disj = [
                Client.full_name.ilike(like),
                Client.email.ilike(like),
                Client.phone_number.ilike(like),
                Client.fact_address.ilike(like),
                phone_norm.ilike(func.regexp_replace(like, r'[^0-9]', '', 'g')),
            ]
            # exact UUID match if looks like uuid
            try:
                uid = UUID(t)
                disj.append(Client.id == uid)
            except Exception:
                pass
            and_groups.append(or_(*disj))
        return and_(*and_groups)

    # ---------- buckets with TRUE totals ----------
    @handle_exceptions()
    async def get_bucket_clients(
            self, skip: int = 0, limit: int = 20, search: Optional[str] = None, deleted: DeletedFilter = "all"
    ) -> Tuple[list[ClientAdminOut], int]:
        where_clause = self._clients_search_clause(search) if search else None
        rows, total = await self._paginate_with_total(
            Client,
            skip=skip,
            limit=limit,
            where_clause=where_clause,
            options=(
                selectinload(Client.worker),
                selectinload(Client.broker),
                selectinload(Client.credits),
            ),
            order_by=Client.created_at.desc(),
            deleted=deleted,  # ⟵ нове
        )
        return [ClientAdminOut.model_validate(r) for r in rows], total

    @handle_exceptions()
    async def get_bucket_brokers(
            self, skip: int = 0, limit: int = 20, deleted: DeletedFilter = "all"
    ) -> Tuple[list[BrokerAdminOut], int]:
        rows, total = await self._paginate_with_total(
            Broker,
            skip=skip,
            limit=limit,
            where_clause=None,
            order_by=Broker.created_at.desc(),
            deleted=deleted,  # ⟵ нове
        )
        return [BrokerAdminOut.model_validate(r) for r in rows], total

    @handle_exceptions()
    async def get_bucket_workers(
            self, skip: int = 0, limit: int = 20, deleted: DeletedFilter = "all"
    ) -> Tuple[list[WorkerAdminOut], int]:
        rows, total = await self._paginate_with_total(
            Worker,
            skip=skip,
            limit=limit,
            where_clause=None,
            order_by=Worker.created_at.desc(),
            deleted=deleted,  # ⟵ нове
        )
        return [WorkerAdminOut.model_validate(r) for r in rows], total

    # ─────────────────────────────
    # 🔍 SINGLE-ENTITY FETCH
    # ─────────────────────────────

    async def _get_one(self, model, entity_id: UUID, *options):
        stmt = select(model).where(model.id == entity_id).options(*options)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    @handle_exceptions()
    async def get_client(self, client_id: UUID) -> ClientAdminOut | None:
        client = await self._get_one(
            Client, client_id, selectinload(Client.worker), selectinload(Client.broker), selectinload(Client.credits)
        )
        if client is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return ClientAdminOut.model_validate(client)

    @handle_exceptions()
    async def get_worker(self, worker_id: UUID) -> WorkerAdminOut | None:
        worker = await self._get_one(Worker, worker_id, selectinload(Worker.clients))
        if worker is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
        return WorkerAdminOut.model_validate(worker)

    @handle_exceptions()
    async def get_broker(self, broker_id: UUID) -> BrokerAdminOut | None:
        broker = await self._get_one(Broker, broker_id, selectinload(Broker.clients))
        if broker is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Broker not found")
        return BrokerAdminOut.model_validate(broker)

    # ─────────────────────────────
    # 🗑 ADMIN ACTIONS
    # ─────────────────────────────

    @handle_exceptions()
    async def delete_user(self, user_id: UUID) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(is_deleted=True, deleted_at=datetime.utcnow())
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def restore_user(self, user_id: UUID, *, reactivate: bool = False) -> None:
        values = dict(is_deleted=False, deleted_at=None)
        if reactivate:
            values["is_active"] = True

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**values)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # ── REASSIGNMENT ────────────────────

    # backend/app/services/entities/admin/admin_dashboard.py
    from fastapi import HTTPException, status

    @handle_exceptions()
    async def worker_reassign_client_by_email(self, client_id: UUID, worker_email: str | None) -> None:
        new_worker_id = None
        if worker_email:
            worker = await WorkerService(self.db).get_by_email(worker_email)  # ✅ інстанс
            if not worker:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
            new_worker_id = worker.id

        await self.db.execute(
            update(Client)
            .where(Client.id == client_id)
            .values(
                worker_id=new_worker_id,
                taken_at_worker=datetime.utcnow() if new_worker_id else None,
            )
            .execution_options(synchronize_session=False)
        )
        await self.db.commit()

    @handle_exceptions()
    async def broker_reassign_client_by_email(self, client_id: UUID, broker_email: str | None) -> None:
        new_broker_id = None
        if broker_email:
            broker = await BrokerService(self.db).get_by_email(broker_email)
            if not broker:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Broker not found")
            new_broker_id = broker.id

        await self.db.execute(
            update(Client)
            .where(Client.id == client_id)
            .values(
                broker_id=new_broker_id,
                taken_at_broker=datetime.utcnow() if new_broker_id else None,
            )
            .execution_options(synchronize_session=False)
        )
        await self.db.commit()

    # ── CREDIT CONTROL ─────────────────

    @handle_exceptions()
    async def force_complete_credit(self, credit_id: UUID) -> None:
        stmt = (
            update(Credit)
            .where(Credit.id == credit_id)
            .values(
                paid_amount=Credit.total_amount,
                status="completed",
                last_payment_at=datetime.now(UTC),
            )
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def change_credit_status(self, credit_id: UUID, new_status: str) -> None:
        stmt = (
            update(Credit)
            .where(Credit.id == credit_id)
            .values(status=new_status)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    # ── EDIT DATA HELPERS ───────────────

    async def _edit_user_and_entity(self, model, entity_id: UUID, fields: Mapping[str, Any]) -> None:
        if not fields:
            return

        # 1) відокремлюємо поля, що лежать у users
        user_fields = {}
        for key in ("email", "is_active"):  # тут можеш додати інші user-поля за потреби
            if key in fields:
                user_fields[key] = fields[key]

        # Якщо міняємо email клієнта — тримаємо синхрон з clients.email
        # (у тебе є і users.email, і clients.email).
        model_fields = dict(fields)
        if model is Client and "email" in user_fields and "email" not in model_fields:
            model_fields["email"] = user_fields["email"]

        # 2) апдейти
        if user_fields:
            await self.db.execute(
                update(User)
                .where(User.id == entity_id)
                .values(**user_fields)
                .execution_options(synchronize_session=False)
            )

        # прибираємо user-поля, щоб не полетіли в модельну таблицю
        for k in user_fields.keys():
            model_fields.pop(k, None)

        if model_fields:
            await self.db.execute(
                update(model)
                .where(model.id == entity_id)
                .values(**model_fields)
                .execution_options(synchronize_session=False)
            )

        # 3) один commit
        await self.db.commit()

    @handle_exceptions()
    async def edit_client_data(self, client_id: UUID, fields: Mapping[str, Any]) -> None:
        await self._edit_user_and_entity(Client, client_id, fields)

    @handle_exceptions()
    async def edit_broker_data(self, broker_id: UUID, fields: Mapping[str, Any]) -> None:
        await self._edit_user_and_entity(Broker, broker_id, fields)

    @handle_exceptions()
    async def edit_worker_data(self, worker_id: UUID, fields: Mapping[str, Any]) -> None:
        await self._edit_user_and_entity(Worker, worker_id, fields)

    def _dialect(self) -> str:
        # "postgresql", "sqlite", ...
        return (self.db.bind and self.db.bind.dialect.name) or "postgresql"

    @handle_exceptions()
    async def get_credits_for_month(self, month: str) -> list[dict[str, Any]]:
        # month = "YYYY-MM"
        try:
            year, month_num = map(int, month.split("-"))
            start_date = date(year, month_num, 1)
            end_date = date(year + (1 if month_num == 12 else 0),
                            1 if month_num == 12 else month_num + 1, 1)
        except Exception:
            raise ValueError("Invalid month format. Expected YYYY-MM.")

        # ключ групування "день"
        if self._dialect() == "sqlite":
            day_key = func.strftime("%Y-%m-%d", Credit.issued_at)  # -> str
        else:
            day_key = func.date(Credit.issued_at)                  # -> date

        stmt = (
            select(day_key.label("d"), func.coalesce(func.sum(Credit.amount), 0).label("total"))
            .where(
                and_(
                    Credit.issued_at >= start_date,
                    Credit.issued_at < end_date,
                    Credit.is_deleted.is_(False),
                )
            )
            .group_by(day_key)
            .order_by(day_key)
        )
        res = await self.db.execute(stmt)
        rows = res.all()

        # мапимо за датою; SQLite повертає рядок, PG — date
        totals_by_day: dict[date, float] = {}
        for d_val, total in rows:
            d = date.fromisoformat(d_val) if isinstance(d_val, str) else d_val
            totals_by_day[d] = float(total or 0.0)

        # повертаємо повний місяць з нулями на порожні дні
        out: list[dict[str, Any]] = []
        for i in range((end_date - start_date).days):
            cur = start_date + timedelta(days=i)
            out.append({"date": cur.isoformat(), "amount": round(totals_by_day.get(cur, 0.0), 2)})
        return out

    @handle_exceptions()
    async def get_credits_for_year(self, year: int) -> list[dict[str, Any]]:
        # ключ групування "місяць" і умова на рік — крос-діалектно
        if self._dialect() == "sqlite":
            month_key = func.cast(func.strftime("%m", Credit.issued_at), int)  # "01".."12" -> int
            year_cond = func.strftime("%Y", Credit.issued_at) == str(year)
        else:
            month_key = func.extract("month", Credit.issued_at)  # 1..12
            year_cond = func.extract("year", Credit.issued_at) == year

        stmt = (
            select(month_key.label("m"), func.coalesce(func.sum(Credit.amount), 0).label("total"))
            .where(and_(year_cond, Credit.is_deleted.is_(False)))
            .group_by(month_key)
            .order_by(month_key)
        )
        res = await self.db.execute(stmt)
        rows = res.all()

        totals_by_month: dict[int, float] = {int(m): float(t or 0.0) for m, t in rows}

        data: list[dict[str, Any]] = []
        for m in range(1, 13):
            data.append({"month": f"{m:02d}", "amount": round(totals_by_month.get(m, 0.0), 2)})
        return data

    @handle_exceptions()
    async def get_count_active_credits(self) -> int:
        stmt = (
            select(func.count(Credit.id))
            .where(Credit.status != CreditStatus.COMPLETED)
            .where(Credit.is_deleted.is_(False))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_count_completed_credits(self) -> int:
        stmt = (
            select(func.count(Credit.id))
            .where(Credit.status == CreditStatus.COMPLETED)
            .where(Credit.is_deleted.is_(False))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    # ─────────────────────────────
    # 🔎 FILTER BUCKETS (with is_deleted)
    # ─────────────────────────────

    @handle_exceptions()
    async def filter_bucket_clients(
        self,
        skip: int = 0,
        limit: int = 6,
        *,
        email: str | None = None,
        phone_number: str | None = None,
        full_name: str | None = None,
        is_deleted: bool | None = None,
    ) -> tuple[list[ClientBrokerOut], int]:
        """
        Вернуть (список, total) клиентов с фильтрами и пагинацией.
        Поддерживает фильтр по удалённости записи: is_deleted = True/False/None.
        """
        conditions = []

        if email:
            conditions.append(Client.email.ilike(f"%{email}%"))
        if phone_number:
            conditions.append(Client.phone_number.ilike(f"%{phone_number}%"))
        if full_name:
            conditions.append(Client.full_name.ilike(f"%{full_name}%"))
        if is_deleted is not None:
            conditions.append(Client.is_deleted.is_(is_deleted))

        where_clause = and_(*conditions) if conditions else True

        total_stmt = select(func.count()).select_from(Client).where(where_clause)
        total_res  = await self.db.execute(total_stmt)
        total: int = total_res.scalar_one()

        data_stmt = (
            select(Client)
            .where(where_clause)
            .options(
                selectinload(Client.worker),
                selectinload(Client.broker),
                selectinload(Client.credits),
            )
            .order_by(Client.full_name.asc())
            .offset(skip)
            .limit(limit)
        )

        data_res = await self.db.execute(data_stmt)
        clients: Sequence[Client] = data_res.scalars().all()

        return (
            [ClientBrokerOut.model_validate(c) for c in clients],
            total,
        )

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
        """
        Вернуть (список, total) работников с фильтрами и пагинацией.
        """
        conditions = []
        if email:
            conditions.append(Worker.email.ilike(f"%{email}%"))
        if username:
            conditions.append(Worker.username.ilike(f"%{username}%"))
        if is_deleted is not None:
            conditions.append(Worker.is_deleted.is_(is_deleted))

        where_clause = and_(*conditions) if conditions else True

        total_stmt = select(func.count()).select_from(Worker).where(where_clause)
        total_res  = await self.db.execute(total_stmt)
        total: int = total_res.scalar_one()

        data_stmt = (
            select(Worker)
            .where(where_clause)
            .order_by(Worker.username.asc())
            .offset(skip)
            .limit(limit)
        )

        data_res = await self.db.execute(data_stmt)
        workers: Sequence[Worker] = data_res.scalars().all()

        return (
            [WorkerAdminOut.model_validate(c) for c in workers],
            total,
        )

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
        """
        Вернуть (список, total) брокеров с фильтрами и пагинацией.
        """
        conditions = []
        if email:
            conditions.append(Broker.email.ilike(f"%{email}%"))
        if company_name:
            conditions.append(Broker.company_name.ilike(f"%{company_name}%"))
        if region:
            subquery = select(literal_column("1")).where(
                literal_column("region_item").ilike(f"%{region}%")
            ).select_from(func.unnest(Broker.region).alias("region_item"))
            conditions.append(exists(subquery))
        if is_deleted is not None:
            conditions.append(Broker.is_deleted.is_(is_deleted))

        where_clause = and_(*conditions) if conditions else True

        total_stmt = select(func.count()).select_from(Broker).where(where_clause)
        total_res  = await self.db.execute(total_stmt)
        total: int = total_res.scalar_one()

        data_stmt = (
            select(Broker)
            .where(where_clause)
            .order_by(Broker.company_name.asc())
            .offset(skip)
            .limit(limit)
        )

        data_res = await self.db.execute(data_stmt)
        brokers: Sequence[Broker] = data_res.scalars().all()

        return (
            [BrokerAdminOut.model_validate(c) for c in brokers],
            total,
        )

    # ─────────────────────────────
    # 🎯 PROMOTIONS (CRUD + Analytics)
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(promo, k, v)
        await self.db.commit()
        await self.db.refresh(promo)
        return promo

    @handle_exceptions()
    async def deactivate_promotion(self, promo_id: UUID) -> None:
        promo = await self.db.get(Promotion, promo_id)
        if not promo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        promo.is_active = False
        await self.db.commit()

    @handle_exceptions()
    async def activate_promotion(self, promo_id: UUID, *, deactivate_others_same_type: bool = False) -> Promotion:
        promo = await self.db.get(Promotion, promo_id)
        if not promo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")

        if deactivate_others_same_type:
            await self.db.execute(
                update(Promotion)
                .where(
                    Promotion.id != promo_id,
                    Promotion.promotion_type == promo.promotion_type,
                    Promotion.is_active.is_(True),
                )
                .values(is_active=False)
                .execution_options(synchronize_session=False)
            )

        promo.is_active = True
        await self.db.commit()
        await self.db.refresh(promo)
        return promo

    @handle_exceptions()
    async def list_promotions(self, *, is_active: bool | None = None, ptype: PromotionEnum | None = None, limit: int = 50) -> list[Promotion]:
        stmt = select(Promotion).order_by(Promotion.created_at.desc()).limit(limit)
        if is_active is not None:
            stmt = stmt.where(Promotion.is_active.is_(is_active))
        if ptype is not None:
            stmt = stmt.where(Promotion.promotion_type == ptype)
        return list((await self.db.execute(stmt)).scalars().all())

    @handle_exceptions()
    async def list_promotions_summary(self, *, ptype: PromotionEnum | None = None, limit: int = 12) -> list[PromotionSummaryOut]:
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        return promo

    @handle_exceptions()
    async def top_workers_by_count(self, *, limit: int = 3) -> list[TopWorkerOut]:
        stmt = (
            select(
                Credit.worker_id.label("worker_id"),
                Worker.username.label("username"),
                func.count(Credit.id).label("credits_count"),
            )
            .join(Worker, Worker.id == Credit.worker_id)
            .where(Credit.worker_id.isnot(None))
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
