FROM node:18.19 AS build

WORKDIR /app

# Copiar solo los archivos necesarios para el build
COPY package.json angular.json tsconfig*.json ./
COPY src/ ./src

# Instalar dependencias de forma reproducible
RUN npm ci

# Construir la aplicación en modo producción
RUN npm run build -- --configuration production

FROM nginx:alpine
# Exponer el puerto donde Nginx sirve contenido estático
EXPOSE 80

# Copiar todos los archivos generados al directorio de Nginx
COPY --from=build /app/dist/status-page/ /usr/share/nginx/html/

# Configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Arrancar Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]