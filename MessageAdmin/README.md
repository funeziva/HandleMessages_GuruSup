# MessageAdmin Microservicio

Servicio para la administración de mensajes con integración de OpenAI.

## Requisitos

- Docker y Docker Compose
- Python 3.9+

## Inicio rápido

1. Inicia MongoDB con Docker Compose:

```bash
# Desde la carpeta MessageAdmin
docker-compose up -d mongodb

# Verificar que MongoDB está funcionando
docker ps
```

2. Configura las variables de entorno:
   - Edita el archivo `src/.env` con la configuración necesaria

3. Ejecuta el servicio:

```bash
# Desde la carpeta MessageAdmin/src
python main.py
```

## Estructura del proyecto

```
MessageAdmin/
├── docker-compose.yml  # Configuración de Docker para servicios
├── src/
│   ├── application/    # Lógica de aplicación y casos de uso
│   ├── config/         # Configuraciones del sistema
│   ├── domain/         # Modelos de dominio
│   ├── infrastructure/ # Implementaciones técnicas y adaptadores
│   ├── tests/          # Pruebas del sistema
│   ├── .env            # Variables de entorno
│   └── main.py         # Punto de entrada de la aplicación
└── README.md
```

## Conexión a MongoDB

La aplicación se conectará automáticamente a MongoDB usando la configuración definida en el archivo `.env`:

- URL por defecto: `mongodb://localhost:27017`
- Base de datos: `message_admin` 