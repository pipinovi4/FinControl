# ---------- BUILD ----------
FROM node:22-alpine AS build

WORKDIR /app

# Кеш для залежностей
COPY package*.json ./
RUN npm install --omit=dev

COPY . .

# Включає Next.js прод-режим під час білду
ENV NODE_ENV=production

# Продукційний білд зі standalone вкладенням
RUN npm run build


# ---------- RUNTIME ----------
FROM node:22-alpine AS runtime

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Копіюємо standalone сервер
COPY --from=build /app/.next/standalone ./
# Копіюємо статичні ресурси
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
