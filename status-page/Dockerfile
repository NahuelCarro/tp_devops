FROM node:16.20-alpine AS build

WORKDIR /app

# Copy project files
COPY package.json angular.json tsconfig*.json ./
COPY src/ ./src

# Install dependencies
RUN npm install --legacy-peer-deps

# Build the Angular project explicitly by name in production mode
RUN npx ng build status-page --configuration production

FROM nginx:alpine

# Custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built browser assets into Nginx's html directory
COPY --from=build /app/dist/status-page/browser/ /usr/share/nginx/html/

# Expose HTTP port
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
