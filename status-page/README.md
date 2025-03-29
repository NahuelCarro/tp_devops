# Página de Estado de Servicios

Página de estado simple para monitorear los servicios de Apostador y Carrera.

## Características

- Muestra el estado actual de cada servicio (Operational, Degraded, Down)
- Muestra el porcentaje de uptime de los últimos 90 días
- Historial de uptime visual
- Verificación automática del estado de los servicios cada minuto

## Requisitos

- Node.js (versión 16 o superior)
- npm (versión 8 o superior)

## Instalación

1. Clonar este repositorio
2. Instalar dependencias:

```bash
cd status-page
npm install
```

3. Configurar la URL base de la API en `src/app/services/status.service.ts`

```typescript
private apiBaseUrl = 'http://localhost:8000'; // Cambiar a la URL correcta
```

## Ejecución en desarrollo

```bash
npm start
```

La aplicación estará disponible en `http://localhost:4200`.

## Compilación para producción

```bash
npm run build
```

Los archivos compilados estarán en el directorio `dist/`.

## Personalización

Puedes personalizar los siguientes aspectos:

- Endpoints de verificación en `status.service.ts`
- Frecuencia de verificación modificando el valor `60000` (60 segundos) en `status.service.ts`
- Estilos y colores en `styles.css` 