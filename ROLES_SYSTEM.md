# 🎭 Sistema de Roles - Tienda de Ropa API

## Descripción

Sistema de roles implementado para controlar el acceso y permisos de usuarios en la aplicación de tienda de ropa.

## Roles Disponibles

### 1. 👤 Usuario (Nivel 1)
- **Descripción**: Usuario básico de la aplicación
- **Permisos**:
  - Ver productos
  - Buscar productos
  - Filtrar productos
  - Ver detalles de productos
  - Iniciar sesión

### 2. ✏️ Editor (Nivel 2)
- **Descripción**: Puede editar contenido y gestionar productos
- **Permisos**:
  - Todos los permisos de Usuario
  - Agregar productos
  - Editar productos
  - Eliminar productos
  - Gestionar categorías

### 3. 👑 Administrador (Nivel 3)
- **Descripción**: Acceso completo al sistema
- **Permisos**:
  - Todos los permisos de Editor
  - Gestionar usuarios
  - Cambiar roles de usuarios
  - Acceso a estadísticas
  - Configuración del sistema

## Jerarquía de Roles

```
Administrador (3) > Editor (2) > Usuario (1)
```

- Los roles superiores incluyen automáticamente los permisos de los roles inferiores
- Un administrador puede realizar todas las acciones de editor y usuario
- Un editor puede realizar todas las acciones de usuario

## Endpoints de la API

### Autenticación
```http
POST /api/auth/login
{
  "username": "usuario@email.com",
  "password": "contraseña"
}
```

**Respuesta**:
```json
{
  "success": true,
  "user": {
    "id": "user_id",
    "username": "usuario@email.com",
    "role": "usuario",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Gestión de Usuarios

#### Crear Usuario
```http
POST /api/users
{
  "username": "nuevo@email.com",
  "password": "contraseña",
  "role": "usuario"
}
```

#### Actualizar Rol
```http
PUT /api/users/role
{
  "username": "usuario@email.com",
  "new_role": "editor"
}
```

#### Obtener Usuarios por Rol
```http
GET /api/users/role/{role}
```

#### Verificar Permisos
```http
POST /api/users/permission
{
  "username": "usuario@email.com",
  "required_role": "editor"
}
```

#### Obtener Roles Disponibles
```http
GET /api/users/roles
```

## Scripts de Utilidad

### 1. Migrar Usuarios Existentes
```bash
python migrate_roles.py
```
- Asigna rol "usuario" a usuarios existentes sin rol
- Crea usuarios de ejemplo con diferentes roles

### 2. Agregar Usuario Interactivo
```bash
python add_user.py
```
- Interfaz interactiva para crear usuarios
- Permite seleccionar rol durante la creación

### 3. Probar Sistema de Roles
```bash
python test_roles.py
```
- Ejecuta pruebas completas del sistema de roles
- Verifica login, permisos y funcionalidades

## Usuarios de Ejemplo

Después de ejecutar `migrate_roles.py`:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin@tienda.com | admin123 | administrador |
| editor@tienda.com | editor123 | editor |
| usuario@tienda.com | usuario123 | usuario |

## Implementación en el Frontend

### Verificar Rol del Usuario
```javascript
// Después del login exitoso
const userRole = response.user.role;

if (userRole === 'administrador') {
  // Mostrar opciones de administración
} else if (userRole === 'editor') {
  // Mostrar opciones de edición
} else {
  // Mostrar opciones básicas de usuario
}
```

### Control de Acceso
```javascript
const hasPermission = (userRole, requiredRole) => {
  const roleLevels = {
    'usuario': 1,
    'editor': 2,
    'administrador': 3
  };
  
  return roleLevels[userRole] >= roleLevels[requiredRole];
};

// Ejemplo de uso
if (hasPermission(userRole, 'editor')) {
  // Mostrar botón de editar
}
```

## Base de Datos

### Estructura de Usuario
```json
{
  "_id": "ObjectId",
  "username": "usuario@email.com",
  "password": "hash_contraseña",
  "role": "usuario",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "is_active": true
}
```

## Seguridad

- Las contraseñas deben ser hasheadas (implementar bcrypt)
- Validar roles en el backend antes de permitir acciones
- Usar tokens JWT para mantener sesiones
- Implementar rate limiting para prevenir ataques

## Próximos Pasos

1. **Implementar JWT**: Tokens de autenticación seguros
2. **Hash de Contraseñas**: Usar bcrypt para seguridad
3. **Middleware de Roles**: Verificar permisos automáticamente
4. **Auditoría**: Log de acciones por rol
5. **Frontend**: Interfaz para gestión de usuarios y roles
