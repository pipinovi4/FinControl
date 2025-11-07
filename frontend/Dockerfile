# ---------- 1️⃣ BUILD STAGE ----------
# Use a lightweight Node.js image for the build process
FROM node:22.17.1-alpine AS build

# Set working directory inside the container
WORKDIR /app

# Copy only dependency files first (to leverage Docker cache)
COPY package*.json ./

# Install only production dependencies for optimal build size
RUN npm ci --omit=dev

# Copy the rest of the source code into the container
COPY . .

# Build the Next.js application (creates the .next directory)
RUN npm run build


# ---------- 2️⃣ RUNTIME STAGE ----------
# Use another lightweight Node.js image for the final runtime environment
FROM node:22.17.1-alpine AS runtime

# Set working directory
WORKDIR /app

# Install only the production dependencies needed to run the app
COPY package*.json ./
RUN npm ci --omit=dev

# Copy build artifacts and essential files from the previous build stage
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/next.config.js ./next.config.js

# Define environment variables for production mode
ENV NODE_ENV=production
ENV PORT=3000

# Expose port 3000 to allow external access
EXPOSE 3000

# Start the Next.js production server
CMD ["npm", "run", "start"]
