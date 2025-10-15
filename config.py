import os

# Configuración de MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/")
DB_NAME = os.getenv("DB_NAME", "login")
COLLECTION_USERS = "users"
COLLECTION_PRODUCTS = "products"
