
---

## **Sprint 2025‑06‑16 → 2025‑06‑30**

| # | Task                                                                                                      | Assignee | Status |
| - | --------------------------------------------------------------------------------------------------------- | -------- | ------ |
| 1 | \[BE] Convert `routes/entities` to factory‑based routers, remove per‑role duplication (BE‑ROUTES‑001)     | @dev     | ✅      |
| 2 | \[BE] Extract role‑specific logic into dedicated handlers to keep SRP (BE‑ROUTES‑002)                     | @dev     | ✅      |
| 3 | \[BE] Move `routes/auth/__init__.py` logic into `routes/auth/factory.py` and update imports (BE‑AUTH‑001) | @dev     | ✅      |
| 4 | **\[BE] Implement Cookies & Tokens for authentication** (BE‑AUTH‑002)                                     | @dev     | ✅      |
| 5 | **\[BE] Create custom auth for bot** (BE‑AUTH‑003)                                                        | @dev     | ✅      |
| 6 | **\[BE] Implement WebSockets for analyze endpoints** (BE‑WS‑001)                                          | @dev     | ✅      |

---

### **New Tasks**

1. **Cookies & Tokens**: **Finalize the implementation of cookies and tokens for authentication, ensuring everything works smoothly**.
   **Status**: ✅ Completed

2. **WebSockets**: Implement WebSocket functionality for analyze endpoints, enabling real-time analytics or live updates.
   **Status**: ✅ **Completed**

3. **Backend Tests**: Write comprehensive tests to validate the backend functionality.
   **Status**: 🟨 In Progress

   * **3.1** **System tests (smoke tests)**: Test basic system endpoints like `/ping` and `/routes-info`
     **Status**: ✅ Completed

   * **3.2** **Auth tests**: Test login, registration, password reset, token handling, and cookies for all roles (admin, worker, broker, client).
     **Status**: ✅ Completed

   * **3.3** **CRUD tests for client entities**: Test CRUD functionality for client roles, including creation, reading, updating, deleting, and filters.
     **Status**: 🟨 In Progress

   * **3.4** **Analyze tests**: Test analytics functionality with role-based restrictions (admin-only analytics, and restricted access for other roles).
     **Status**: 🟨 Pending

   * **3.5** **WebSocket tests**: Test WebSocket endpoints for real-time analytics and message handling.
     **Status**: 🟨 Pending

4. **Bot Development**: Once the backend is fully tested, focus on building the Telegram bot and integrating it with the backend.
   **Status**: ⬜ Pending

5. **Frontend**: After the bot, move on to developing the frontend. This will require communication with the backend, so ensure it's prepared to handle dynamic routes.
   **Status**: ⬜ Pending

6. **Active Sockets & Routes Endpoint**: Create a route that will provide the list of active sockets and routes, allowing the frontend to be aware of the status of the backend on initialization.
   **Status**: ✅ **Completed**

---

### **Updated**:

* **WebSocket layer** is fully implemented with dedicated middleware, exception handling, and analyze endpoints routing.
* **Cookies & Tokens** (BE‑AUTH‑002) finalized and functional.
* **Custom Auth for Bot** (BE‑AUTH‑003) completed with role-based separation.
* **Backend Tests** (BE‑TESTS‑001) are in progress and should cover:

  * **System tests**: `/ping`, `/routes-info`
  * **Auth tests**: Login, register, token handling
  * **CRUD tests**: For clients and other roles
  * **Analyze tests**: With role-based restrictions
  * **WebSocket tests**: For real-time endpoints

---
