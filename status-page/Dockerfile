FROM node:18.19 AS build

WORKDIR /app

# Copy only necessary files for build
COPY package.json angular.json tsconfig*.json ./
COPY src/ ./src

# Install dependencies
RUN npm install

# Build the application for production
RUN npm run build -- --configuration production

FROM nginx:alpine

# Copy custom Nginx configuration (overwrites default)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built artifacts to Nginx's html directory
COPY --from=build /app/dist/status-page/ /usr/share/nginx/html/

# Expose HTTP port
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
