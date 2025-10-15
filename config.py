import os

# Configuración de MongoDB usando variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "login")
COLLECTION_USERS = "users"
COLLECTION_PRODUCTS = "products"

# Validar que las variables de entorno estén configuradas
if not MONGODB_URI:
    raise ValueError("MONGODB_URI no está configurada en las variables de entorno")
