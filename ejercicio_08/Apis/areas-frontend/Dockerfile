# Etapa 1: Construcción de la aplicación Angular
FROM node:20 AS build

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar package.json y package-lock.json e instalar dependencias
COPY package.json package-lock.json ./
RUN npm install

# Copiar el código fuente y compilar Angular
COPY . .
RUN npm run build --prod

# Etapa 2: Servir la aplicación con Nginx
FROM nginx:1.25

# Copiar los archivos compilados de la etapa de construcción
COPY --from=build /app/dist/areas-frontend/browser /usr/share/nginx/html

# Copiar configuración personalizada de Nginx (opcional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto en el que Nginx servirá la aplicación
EXPOSE 80

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
