# ---------- BUILD ----------
FROM node:22-alpine AS build

WORKDIR /app

# 1) Кеш залежностей
COPY package*.json ./
RUN npm install

# 2) ОБОВʼЯЗКОВО копіюємо public ДО build
COPY public ./public

# 3) Копіюємо решту коду
COPY . .

ENV NODE_ENV=production

# 4) Стендалоун білд
RUN npm run build


# ---------- RUNTIME ----------
FROM node:22-alpine AS runtime

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Копіюємо standalone сервер (включає node_modules)
COPY --from=build /app/.next/standalone ./

# Копіюємо статичні файли (для підвантаження)
COPY --from=build /app/.next/static ./.next/static

# Копіюємо public (з білда у runtime)
COPY --from=build /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
