FROM node:18.19 AS build

WORKDIR /app

# Copy necessary files
COPY package.json angular.json tsconfig*.json ./
COPY src/ ./src

# Install dependencies reproducibly
RUN npm ci

# Build the application for production
RUN npm run build -- --configuration production

FROM nginx:alpine

# Expose port where Nginx serves static content
EXPOSE 80

# Copy built artifacts (browser bundle) to Nginx default html directory
COPY --from=build /app/dist/status-page/browser/ /usr/share/nginx/html/

# Custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
