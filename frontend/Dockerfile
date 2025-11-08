# ---------- BUILD ----------
FROM node:22-alpine AS build

WORKDIR /app

# Кеш залежностей
COPY package*.json ./
RUN npm install

# Копіюємо решту коду
COPY . .

ENV NODE_ENV=production

# Білд зі standalone
RUN npm run build


# ---------- RUNTIME ----------
FROM node:22-alpine AS runtime

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Копіюємо standalone сервер (всередині вже є node_modules)
COPY --from=build /app/.next/standalone ./
# Копіюємо статичні файли (ті, що обробляє next)
COPY --from=build /app/.next/static ./.next/static

# ❌ Видалено, бо public/ тобі не потрібний
# COPY --from=build /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
