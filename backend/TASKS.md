
---

## **Sprint 2025‑06‑16 → 2025‑06‑30**

| #  | Task                                                                                                      | Assignee | Status        |
| -- | --------------------------------------------------------------------------------------------------------- | -------- | ------------- |
| 1  | \[BE] Convert `routes/entities` to factory‑based routers, remove per‑role duplication (BE‑ROUTES‑001)     | @dev     | ✅             |
| 2  | \[BE] Extract role‑specific logic into dedicated handlers to keep SRP (BE‑ROUTES‑002)                     | @dev     | ✅             |
| 3  | \[BE] Move `routes/auth/__init__.py` logic into `routes/auth/factory.py` and update imports (BE‑AUTH‑001) | @dev     | ✅             |
| 4  | \[BE] Implement Cookies & Tokens for authentication (BE‑AUTH‑002)                                         | @dev     | ✅             |
| 5  | \[BE] Create custom auth for bot (BE‑AUTH‑003)                                                            | @dev     | ✅             |
| 6  | \[BE] Implement WebSockets for analyze endpoints (BE‑WS‑001)                                              | @dev     | ✅             |
| 7  | \[BE] Create `analyze_router_factory` with role-based schema typing (BE‑ANALYZE‑001)                      | @dev     | ⏳ In Progress |
| 8  | \[BE] Implement core analyze metrics: `clients_growth`, `revenue_per_day` (BE‑ANALYZE‑002)                | @dev     | ⏳ In Progress |
| 9  | \[BE] Validate types, input\_model/response\_model for analyze routes (BE‑ANALYZE‑003)                    | @dev     | ⏳ In Progress |
| 10 | \[BE] Ensure `_meta` response is attached and consistent in analyze replies (BE‑ANALYZE‑004)              | @dev     | ⏳ In Progress |
| 11 | \[FE] Implement frontend: dashboard with tables, filters, and role logic (FE‑DASH‑001)                    | @dev     | ⬜ Pending     |

---

## Поточний пріоритет:

### 🔐 Auth

* [x] Додати login з бота (`/auth/login/bot`)
* [x] Протестити та запушити (✅ done)

### 📊 Analyze

* [ ] Перевірити типи в `analyze_router_factory` (role, AnalyzeType, Service, FilterSchema)
* [ ] Додати `response_model` та `input_model`
* [ ] Перевірити `_meta` у відповіді
* [ ] Реалізувати 1–2 метрики (`run_clients_growth`, `run_revenue_per_day`)

### 🎨 Frontend

* [ ] Почати писати фронт (Next.js + Tailwind)
* [ ] Реалізувати dashboard з таблицями, фільтрами, логікою ролей

---
