FROM node:18.19 AS build

# Add build arguments for proxy and npm config
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NPM_CONFIG_REGISTRY
ARG NPM_CONFIG_STRICT_SSL
ARG NPM_CONFIG_TIMEOUT

WORKDIR /app

# Copy project files
COPY package.json angular.json tsconfig*.json ./
COPY src/ ./src

# Configure npm with proxy and registry settings
RUN npm config set proxy $HTTP_PROXY \
    && npm config set https-proxy $HTTPS_PROXY \
    && npm config set registry ${NPM_CONFIG_REGISTRY:-https://registry.npmjs.org/} \
    && npm config set strict-ssl ${NPM_CONFIG_STRICT_SSL:-false} \
    && npm config set fetch-timeout ${NPM_CONFIG_FETCH_TIMEOUT:-100000} \
    && npm config set fetch-retry-mintimeout ${NPM_CONFIG_FETCH_RETRY_MINTIMEOUT:-20000} \
    && npm config set fetch-retry-maxtimeout ${NPM_CONFIG_FETCH_RETRY_MAXTIMEOUT:-120000}

# Install dependencies with additional reliability flags
RUN npm install --verbose --no-audit --no-fund --maxsockets=1

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
