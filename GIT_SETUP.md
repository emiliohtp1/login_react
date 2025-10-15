# 📦 Archivos para Subir a Git

## ✅ Archivos Necesarios para Render.com

Estos son los archivos que debes subir a tu repositorio de Git:

### 📄 Archivos de Configuración
- `requirements.txt` - Dependencias de Python
- `render.yaml` - Configuración de Render.com
- `.gitignore` - Archivos a ignorar en Git
- `env.example` - Ejemplo de variables de entorno

### 🐍 Archivos de Código Python
- `main.py` - Punto de entrada para Render
- `api_server.py` - Servidor FastAPI
- `database_manager.py` - Gestor de MongoDB
- `config.py` - Configuración de la aplicación

### 📚 Archivos de Documentación
- `README.md` - Documentación general
- `DEPLOY.md` - Guía de despliegue
- `GIT_SETUP.md` - Este archivo

### 🛠️ Archivos Opcionales (útiles para desarrollo)
- `add_user.py` - Script para agregar usuarios
- `setup_database.py` - Script de inicialización
- `test_connection.py` - Script de prueba

## 🚫 Archivos que NO debes subir

- `__pycache__/` - Cache de Python (ya está en .gitignore)
- `.env` - Variables de entorno locales (ya está en .gitignore)
- `*.pyc` - Archivos compilados de Python

## 📝 Comandos de Git

### Inicializar repositorio (si no existe)
```bash
cd python_db
git init
```

### Agregar archivos
```bash
git add .
```

### Hacer commit
```bash
git commit -m "API FastAPI para Tienda de Ropa"
```

### Conectar con repositorio remoto
```bash
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
```

### Subir a GitHub
```bash
git push -u origin main
```

## 🔐 Seguridad

**IMPORTANTE:** Las credenciales de MongoDB ya están en `render.yaml` para facilitar el despliegue, pero deberías:

1. **Eliminar las credenciales de `render.yaml`** antes de subir a un repositorio público
2. **Usar las variables de entorno de Render** en su lugar
3. **Configurar las variables en el Dashboard de Render** manualmente

### Versión segura de render.yaml

```yaml
services:
  - type: web
    name: tienda-ropa-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: MONGODB_URI
        sync: false  # Configurar manualmente en Render
      - key: DB_NAME
        value: login
      - key: PYTHON_VERSION
        value: 3.9.0
```

## 📋 Checklist antes de subir

- [ ] Verificar que `.gitignore` está presente
- [ ] Revisar que no hay credenciales sensibles en el código
- [ ] Probar localmente que la API funciona
- [ ] Actualizar `README.md` si es necesario
- [ ] Hacer commit con un mensaje descriptivo

## 🎯 Siguiente Paso

Una vez subido a Git, sigue la guía en `DEPLOY.md` para desplegar en Render.com.

