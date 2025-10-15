# 🚀 Inicio Rápido - Despliegue en Render.com

## ⚡ Pasos Rápidos

### 1️⃣ Subir a Git (5 minutos)

```bash
cd python_db
git init
git add .
git commit -m "API FastAPI - Tienda de Ropa"
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git push -u origin main
```

### 2️⃣ Desplegar en Render (5 minutos)

1. Ve a https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Conecta tu repositorio
4. Configura:
   - **Name:** `tienda-ropa-api`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Plan:** Free

5. Agrega variables de entorno:
   ```
   MONGODB_URI = mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/
   DB_NAME = login
   ```

6. Click "Create Web Service"

### 3️⃣ Obtener URL

Render te dará una URL como:
```
https://tienda-ropa-api.onrender.com
```

### 4️⃣ Actualizar App React

En `src/services/database.ts`, cambia:

```typescript
const API_BASE_URL = 'https://TU-URL-DE-RENDER.onrender.com/api';
```

### 5️⃣ Probar

Visita:
- `https://TU-URL-DE-RENDER.onrender.com/` - Página principal
- `https://TU-URL-DE-RENDER.onrender.com/docs` - Documentación interactiva
- `https://TU-URL-DE-RENDER.onrender.com/api/health` - Health check

## ✅ ¡Listo!

Tu API está desplegada y funcionando. 

## 📚 Más Información

- Ver `DEPLOY.md` para guía detallada
- Ver `GIT_SETUP.md` para información sobre Git
- Ver `README.md` para documentación completa

## 🆘 Problemas?

1. **Servicio no inicia:** Revisa los logs en Render Dashboard
2. **Error de MongoDB:** Verifica las credenciales en variables de entorno
3. **CORS error:** Actualiza `allow_origins` en `api_server.py`

## 💡 Nota Importante

El plan gratuito de Render "duerme" después de 15 minutos de inactividad. La primera petición puede tardar 30-60 segundos en responder.

