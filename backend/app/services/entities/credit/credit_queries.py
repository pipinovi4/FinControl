import re
from uuid import UUID

from sqlalchemy import or_, and_, String, func, cast as sa_cast
from app.models.entities.credit import Credit
from app.models.entities.application import Application


def _phone_norm(expr):
    return func.regexp_replace(expr, r"[^0-9]", "", "g")


def looks_uuid(term: str) -> UUID | None:
    try:
        return UUID(term)
    except Exception:
        return None


def search_clause_for_credit(search: str):
    if not search:
        return None

    terms = [t.strip() for t in re.split(r"[\s,]+", search) if t.strip()]
    if not terms:
        return None

    clauses = []
    for term in terms:
        like = f"%{term}%"

        disj = [
            sa_cast(Credit.id, String).ilike(like),

            # JSONB
            Application.data["full_name"].as_string().ilike(like),
            Application.data["email"].as_string().ilike(like),
            Application.data["phone_number"].as_string().ilike(like),

            _phone_norm(Application.data["phone_number"].as_string())
            .ilike(_phone_norm(like)),
        ]

        uuid_val = looks_uuid(term)
        if uuid_val:
            disj.append(Credit.id == uuid_val)
            disj.append(Application.id == uuid_val)

        clauses.append(or_(*disj))

    return and_(*clauses)

__all__ = ["search_clause_for_credit"]