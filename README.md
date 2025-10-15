# 🐍 Gestión de Base de Datos MongoDB

Esta carpeta contiene scripts de Python para gestionar la base de datos MongoDB de la aplicación de tienda de ropa.

## 📋 Archivos

- `database_manager.py` - Clase principal para gestionar la base de datos
- `config.py` - Configuración de conexión a MongoDB
- `add_user.py` - Script para agregar usuarios
- `setup_database.py` - Script para configurar datos iniciales
- `test_connection.py` - Script para probar la conexión
- `requirements.txt` - Dependencias de Python

## 🚀 Instalación

1. **Instalar dependencias:**
   ```bash
   cd python_db
   pip install -r requirements.txt
   ```

2. **Configurar la base de datos:**
   ```bash
   python setup_database.py
   ```

## 📖 Uso

### Agregar un nuevo usuario
```bash
python add_user.py
```

### Probar la conexión
```bash
python test_connection.py
```

### Configurar datos iniciales
```bash
python setup_database.py
```

## 🔧 Configuración

Las credenciales de MongoDB están configuradas en `config.py`:

- **URI:** `mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/`
- **Base de datos:** `login`
- **Colecciones:** `users`, `products`

## 📊 Estructura de Datos

### Usuarios
```json
{
  "username": "admin@tienda.com",
  "password": "admin123",
  "created_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

### Productos
```json
{
  "name": "Camiseta Básica Blanca",
  "price": 25.99,
  "description": "Camiseta de algodón 100%...",
  "category": "Camisetas",
  "image": "https://via.placeholder.com/300x200",
  "size": "M",
  "color": "Blanco",
  "stock": 50,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 🔐 Usuario por Defecto

- **Email:** `admin@tienda.com`
- **Contraseña:** `admin123`

## ⚠️ Notas de Seguridad

- Las credenciales están hardcodeadas para desarrollo
- En producción, usar variables de entorno
- Cambiar las contraseñas por defecto
