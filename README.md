# 📱 Página Web Android Studio

Proyecto de aplicación Android desarrollado por **Isaac Esteban Haro Torres**.

---

## 📝 Descripción

Aplicación móvil desarrollada en Android Studio.

---

## ✨ Características

- Interfaz de usuario Android
- Navegación entre pantallas
- Consumo de APIs
- Base de datos local

---

## 🛠️ Stack Tecnológico

- Android Studio
- Java / Kotlin
- XML

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack · Automatización · Data**

- 📧 Email: zackharo1@gmail.com
- 📱 WhatsApp: 098805517
- 💻 GitHub: https://github.com/ieharo1
- 🌐 Portafolio: https://ieharo1.github.io/portafolio-isaac.haro/

---

# Sistema de Gestión de Almacén (Warehouse Management System)

FastAPI + MongoDB + Bootstrap 5

---

## Descripción

Sistema completo de gestión de almacén con autenticación JWT, gestión de productos, ubicaciones (Perchas, Pisos, Columnas), estructura del almacén y búsqueda de productos.

---

## Estructura del Proyecto

```
PAGINA-WEB-ANDROID-STUDIO/
├── app/
│   ├── config.py          # Configuración de la aplicación
│   ├── database.py       # Conexión a MongoDB
│   ├── main.py           # Aplicación FastAPI principal
│   ├── schemas/
│   │   └── schemas.py    # Modelos Pydantic
│   ├── services/
│   │   └── auth_service.py  # Autenticación JWT
│   ├── repositories/
│   │   └── repository.py # Operaciones CRUD
│   ├── routes/
│   │   ├── auth.py       # Rutas de autenticación
│   │   └── warehouse.py  # Rutas del almacén
│   └── templates/        # Plantillas HTML
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── dashboard.html
│       ├── products.html
│       ├── locations.html
│       ├── structure.html
│       └── search.html
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.8+
- MongoDB
- Node.js (opcional, para desarrollo)

---

## Instalación

1. Clonar el repositorio y entrar al directorio:
```bash
cd PAGINA-WEB-ANDROID-STUDIO
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar MongoDB (crear archivo `.env` opcional):
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=warehouse_db
SECRET_KEY=your-secret-key
```

5. Iniciar MongoDB:
```bash
mongod
```

6. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload
```

7. Abrir en el navegador:
```
http://localhost:8000
```

---

## Colecciones MongoDB

- `users` - Usuarios del sistema
- `products` - Productos del almacén
- `warehouse_locations` - Ubicaciones (percha, piso, columna)
- `warehouse_structure` - Estructuras del almacén

---

## Características

- Login/Registro con JWT
- Dashboard con estadísticas
- CRUD de Productos
- Gestión de Ubicaciones (Perchas, Pisos, Columnas)
- Estructura del Almacén
- Búsqueda de productos con ubicación exacta
- Interfaz Bootstrap 5 responsiva

---

## API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | / | Página principal |
| GET/POST | /login | Iniciar sesión |
| GET/POST | /register | Registrarse |
| GET | /logout | Cerrar sesión |
| GET | /dashboard | Dashboard |
| GET/POST | /products | Gestión de productos |
| GET/POST | /locations | Gestión de ubicaciones |
| GET/POST | /structure | Gestión de estructura |
| GET/POST | /search | Buscar productos |

---

## Tecnologías

- **Backend:** FastAPI, Python
- **Base de datos:** MongoDB (Motor)
- **Frontend:** Bootstrap 5, Jinja2
- **Auth:** JWT, Passlib

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack · Automatización · Data**

- 📧 Email: zackharo1@gmail.com
- 📱 WhatsApp: 098805517
- 💻 GitHub: https://github.com/ieharo1
- 🌐 Portafolio: https://ieharo1.github.io/portafolio-isaac.haro/

---

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.
