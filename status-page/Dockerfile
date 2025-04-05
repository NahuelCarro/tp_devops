FROM node:18.19 AS build

WORKDIR /app

# Copiar solo los archivos necesarios
COPY package.json ./
COPY angular.json ./
COPY tsconfig*.json ./
COPY src/ src/

# Instalar dependencias (sin package-lock para que use las versiones correctas de Linux)
RUN npm install

# Construir la aplicación
# En caso de querer usar el localmente reemplazar production por development, de esta forma usa el proxy en lugar de la api plana
RUN npm run build -- --configuration production

FROM nginx:alpine
COPY --from=build /app/dist/status-page/browser/* /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]