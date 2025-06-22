# TASKS

## Milestones

* [ ] Route refactor to factory pattern & DRY (15 Jul 2025)
* [ ] Auth router extracted to dedicated factory (15 Jul 2025)

---

## Sprint 2025‑06‑16 → 2025‑06‑30

| # | Task                                                                                                      | Assignee | Status |
| - | --------------------------------------------------------------------------------------------------------- | -------- | ------ |
| 1 | [BE] Convert `routes/entities` to factory‑based routers, remove per‑role duplication (BE‑ROUTES‑001)     | @dev     | ✅      |
| 2 | [BE] Extract role‑specific logic into dedicated handlers to keep SRP (BE‑ROUTES‑002)                     | @dev     | ✅      |
| 3 | [BE] Move `routes/auth/__init__.py` logic into `routes/auth/factory.py` and update imports (BE‑AUTH‑001) | @dev     | ✅      |

---

## Task Details

### BE‑ROUTES‑001  Convert `routes/entities` to factory‑based routers

**Estimate**: 16 h  
**Dependencies**: —  
**Description**

1. Audit duplicated CRUD routers for `ADMIN` / `WORKER` / `BROKER` / `CLIENT`.
2. Implement a generic router factory that takes `Service`, `Schema`, and `PermissionRole`, registering CRUD paths dynamically.
3. Delete obsolete per‑role router files (≈ 20).
4. Add unit tests for generated routers.

**Definition of Done**

* ✅ Duplicate code per entity route < 5 %.
* ✅ All existing integration tests pass.

---

### BE‑ROUTES‑002  Extract role‑specific logic into handlers (SRP)

**Estimate**: 8 h  
**Dependencies**: BE‑ROUTES‑001  
**Description**

1. For each entity, move business rules specific to roles into `handlers/<role>/<entity>.py`.
2. Keep router factories thin; they should only wire HTTP layer to handler calls.

**Definition of Done**

* ✅ Code‑duplication metric (CodeClimate) < 10 %.
* ✅ Handler test coverage ≥ 90 %.

---

### BE‑AUTH‑001  Relocate auth router assembly into factory module

**Estimate**: 4 h  
**Dependencies**: —  
**Description**

1. Create `routes/auth/factory.py` encapsulating `create_login_router` and `create_register_router`.
2. Replace lazy imports with explicit dependency injection where feasible.
3. Update `routes/__init__.py` to import routers from the new factory/config module.

**Definition of Done**

* ✅ No circular‑import warnings at startup.
* ✅ `uvicorn` startup time same or better.

---

## Misc TODO

* [ ] Update developer guide to reflect new router factory usage.

---

### New Tasks

1. **Cookies & Tokens**: Finalize the implementation of cookies and tokens for authentication, ensuring everything works smoothly.
2. **WebSockets**: Implement WebSocket functionality for analyze endpoints, enabling real-time analytics or live updates.
3. **Backend Tests**: Write comprehensive tests to validate the backend functionality.
4. **Bot Development**: Once the backend is fully tested, focus on building the Telegram bot and integrating it with the backend.
5. **Frontend**: After the bot, move on to developing the frontend. This will require communication with the backend, so ensure it's prepared to handle dynamic routes.
6. **Active Sockets & Routes Endpoint**: Create a route that will provide the list of active sockets and routes, allowing the frontend to be aware of the status of the backend on initialization.

---

*Last updated: 2025‑06‑19/13:40*
