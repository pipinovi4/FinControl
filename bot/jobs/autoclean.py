from datetime import datetime, timedelta, UTC

TTL = timedelta(hours=24)  # 24h

# Поля, які НЕ МОЖНА видаляти (персональні настройки юзера)
SAFE_KEYS = {"lang", "country", "region"}

async def cleanup_user_data(context):
    now = datetime.now(UTC)

    store = context.application.user_data  # { user_id: { ... } }
    to_delete_users = []

    for user_id, data in store.items():

        ts = data.get("_ts")
        if not ts:
            # якщо нема timestamp — ставимо його зараз
            data["_ts"] = now
            continue

        # якщо юзер не активний більше ніж TTL
        if now - ts > TTL:
            to_delete_users.append(user_id)
            continue

        # 🔥 часткове очищення для активних сесій:
        # прибираємо тільки "сміття", але зберігаємо мову/країну
        keys_to_remove = [
            key for key in data.keys()
            if key not in SAFE_KEYS and key not in ("_ts",)
        ]

        for key in keys_to_remove:
            data.pop(key, None)

    # Видаляємо повністю протухші user_data
    for uid in to_delete_users:
        store.pop(uid, None)

    if to_delete_users:
        print(f"[AutoClean] Removed {len(to_delete_users)} expired sessions")
