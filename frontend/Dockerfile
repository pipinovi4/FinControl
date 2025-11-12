# ---------- BUILD ----------
FROM node:22-alpine AS build

WORKDIR /app

# 1️⃣ Параметр для білду
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# 2️⃣ Кеш залежностей
COPY package*.json ./
RUN npm install

# 3️⃣ Копіюємо public ДО build
COPY public ./public

# 4️⃣ Копіюємо решту коду
COPY . .

ENV NODE_ENV=production

# 🧠 DEBUG: покажемо значення при білді
RUN echo "🌍 Building frontend with NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL"

# 5️⃣ Стендалоун білд
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

# Копіюємо public
COPY --from=build /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
