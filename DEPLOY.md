# 🚀 Guía de Despliegue en Render.com

Esta guía te ayudará a desplegar la API FastAPI de la Tienda de Ropa en Render.com.

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com) (gratis)
- Repositorio de Git (GitHub, GitLab, o Bitbucket)
- Credenciales de MongoDB Atlas

## 🔧 Paso 1: Preparar el Repositorio

1. **Subir los archivos a Git:**
   ```bash
   cd python_db
   git init
   git add .
   git commit -m "Initial commit - API FastAPI"
   git remote add origin <tu-repositorio>
   git push -u origin main
   ```

## 🌐 Paso 2: Crear el Web Service en Render

1. **Ir a Render Dashboard:**
   - Visita https://dashboard.render.com
   - Click en "New +" → "Web Service"

2. **Conectar el Repositorio:**
   - Selecciona tu repositorio de Git
   - Click en "Connect"

3. **Configurar el Servicio:**
   - **Name:** `tienda-ropa-api` (o el nombre que prefieras)
   - **Environment:** `Python 3`
   - **Region:** Selecciona la más cercana
   - **Branch:** `main`
   - **Root Directory:** `python_db` (si está en una subcarpeta)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Plan:** `Free`

4. **Configurar Variables de Entorno:**
   
   En la sección "Environment Variables", agrega:
   
   | Key | Value |
   |-----|-------|
   | `MONGODB_URI` | `mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/` |
   | `DB_NAME` | `login` |
   | `PYTHON_VERSION` | `3.9.0` |

5. **Desplegar:**
   - Click en "Create Web Service"
   - Espera a que termine el despliegue (5-10 minutos)

## ✅ Paso 3: Verificar el Despliegue

Una vez desplegado, Render te dará una URL como:
```
https://tienda-ropa-api.onrender.com
```

Prueba los endpoints:

1. **Health Check:**
   ```
   https://tienda-ropa-api.onrender.com/api/health
   ```

2. **Documentación Interactiva:**
   ```
   https://tienda-ropa-api.onrender.com/docs
   ```

## 🔗 Paso 4: Conectar con la Aplicación Web

Actualiza el archivo `src/services/database.ts` en tu aplicación React:

```typescript
const API_BASE_URL = 'https://tienda-ropa-api.onrender.com/api';
```

Reemplaza `https://tienda-ropa-api.onrender.com` con tu URL de Render.

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Verificar estado de la API |
| POST | `/api/auth/login` | Autenticar usuario |
| GET | `/api/products` | Obtener todos los productos |
| GET | `/api/products/{id}` | Obtener producto específico |
| POST | `/api/users` | Agregar nuevo usuario |

## 🔒 Seguridad

### Configurar CORS en Producción

Edita `api_server.py` y reemplaza:

```python
allow_origins=["*"]
```

Por:

```python
allow_origins=[
    "https://tu-dominio.com",
    "http://localhost:3000"  # Solo para desarrollo
]
```

### Proteger Credenciales

1. **Nunca subas credenciales al repositorio**
2. **Usa variables de entorno en Render**
3. **Considera usar secretos de MongoDB Atlas**

## 🐛 Solución de Problemas

### Error: "Application failed to respond"
- Verifica que el comando de inicio sea correcto: `python main.py`
- Revisa los logs en Render Dashboard

### Error: "Module not found"
- Asegúrate de que `requirements.txt` esté actualizado
- Verifica el comando de build: `pip install -r requirements.txt`

### Error de conexión a MongoDB
- Verifica las credenciales en las variables de entorno
- Asegúrate de que MongoDB Atlas permita conexiones desde cualquier IP (0.0.0.0/0)

## 📝 Notas Importantes

1. **Plan Gratuito de Render:**
   - El servicio se "duerme" después de 15 minutos de inactividad
   - La primera petición después de dormir puede tardar 30-60 segundos

2. **Actualizaciones Automáticas:**
   - Render despliega automáticamente cuando haces push a la rama principal

3. **Logs:**
   - Puedes ver los logs en tiempo real en el Dashboard de Render

## 🎉 ¡Listo!

Tu API FastAPI ahora está desplegada y lista para usar. Puedes acceder a la documentación interactiva en `/docs` para probar todos los endpoints.

