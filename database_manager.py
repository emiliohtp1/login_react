from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME, DB_NAME_PRUEBA, COLLECTION_USERS, COLLECTION_PRODUCTS, COLLECTION_PRUEBA
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Conectar a MongoDB"""
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DB_NAME]
            print("Conectado a MongoDB exitosamente")
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            raise e
    
    def disconnect(self):
        """Desconectar de MongoDB"""
        if self.client:
            self.client.close()
            print("Desconectado de MongoDB")
    
    def add_user(self, username, password):
        """Agregar un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            existing_user = self.db[COLLECTION_USERS].find_one({"username": username})
            if existing_user:
                return {"success": False, "message": "El usuario ya existe"}
            
            # Crear nuevo usuario
            user_data = {
                "username": username,
                "password": password,
                "created_at": datetime.now(),
                "is_active": True
            }
            
            result = self.db[COLLECTION_USERS].insert_one(user_data)
            
            if result.inserted_id:
                return {
                    "success": True, 
                    "message": f"Usuario '{username}' creado exitosamente",
                    "user_id": str(result.inserted_id)
                }
            else:
                return {"success": False, "message": "Error al crear el usuario"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_user(self, username, password):
        """Obtener usuario por credenciales"""
        try:
            user = self.db[COLLECTION_USERS].find_one({
                "username": username,
                "password": password,
                "is_active": True
            })
            
            if user:
                return {
                    "success": True,
                    "user": {
                        "id": str(user["_id"]),
                        "username": user["username"],
                        "created_at": user["created_at"]
                    }
                }
            else:
                return {"success": False, "message": "Credenciales incorrectas"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_all_users(self):
        """Obtener todos los usuarios"""
        try:
            users = list(self.db[COLLECTION_USERS].find({"is_active": True}))
            return {
                "success": True,
                "users": [
                    {
                        "id": str(user["_id"]),
                        "username": user["username"],
                        "created_at": user["created_at"]
                    } for user in users
                ]
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def add_product(self, product_data):
        """Agregar un nuevo producto"""
        try:
            product_data["created_at"] = datetime.now()
            result = self.db[COLLECTION_PRODUCTS].insert_one(product_data)
            
            if result.inserted_id:
                return {
                    "success": True,
                    "message": "Producto creado exitosamente",
                    "product_id": str(result.inserted_id)
                }
            else:
                return {"success": False, "message": "Error al crear el producto"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_all_products(self):
        """Obtener todos los productos"""
        try:
            products = list(self.db[COLLECTION_PRODUCTS].find())
            return {
                "success": True,
                "products": [
                    {
                        "id": str(product["_id"]),
                        "name": product["name"],
                        "price": product["price"],
                        "description": product["description"],
                        "category": product["category"],
                        "image": product["image"],
                        "size": product["size"],
                        "color": product["color"],
                        "stock": product.get("stock", 0)
                    } for product in products
                ]
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def create_sample_data(self):
        """Crear datos de muestra"""
        try:
            # Crear usuario de prueba
            admin_user = self.add_user("admin@tienda.com", "admin123")
            print(f"Usuario admin: {admin_user['message']}")
            
            # Crear productos de muestra
            sample_products = [
                {
                    "name": "Camiseta Básica Blanca",
                    "price": 25.99,
                    "description": "Camiseta de algodón 100% de alta calidad, perfecta para el día a día.",
                    "category": "Camisetas",
                    "image": "https://via.placeholder.com/300x200/6200ea/ffffff?text=Camiseta+Blanca",
                    "size": "M",
                    "color": "Blanco",
                    "stock": 50
                },
                {
                    "name": "Jeans Clásicos Azules",
                    "price": 59.99,
                    "description": "Jeans de corte clásico en denim azul, cómodos y duraderos.",
                    "category": "Pantalones",
                    "image": "https://via.placeholder.com/300x200/1976d2/ffffff?text=Jeans+Azules",
                    "size": "L",
                    "color": "Azul",
                    "stock": 30
                },
                {
                    "name": "Vestido Elegante Negro",
                    "price": 89.99,
                    "description": "Vestido elegante para ocasiones especiales, corte A-line.",
                    "category": "Vestidos",
                    "image": "https://via.placeholder.com/300x200/424242/ffffff?text=Vestido+Negro",
                    "size": "M",
                    "color": "Negro",
                    "stock": 20
                },
                {
                    "name": "Zapatos Deportivos",
                    "price": 79.99,
                    "description": "Zapatos deportivos cómodos para caminar y hacer ejercicio.",
                    "category": "Zapatos",
                    "image": "https://via.placeholder.com/300x200/ff9800/ffffff?text=Zapatos+Deportivos",
                    "size": "42",
                    "color": "Negro",
                    "stock": 25
                },
                {
                    "name": "Collar de Plata",
                    "price": 45.99,
                    "description": "Collar elegante de plata 925, perfecto para complementar cualquier outfit.",
                    "category": "Accesorios",
                    "image": "https://via.placeholder.com/300x200/9e9e9e/ffffff?text=Collar+Plata",
                    "size": "Único",
                    "color": "Plata",
                    "stock": 15
                },
                {
                    "name": "Sudadera con Capucha",
                    "price": 49.99,
                    "description": "Sudadera cómoda con capucha, ideal para días frescos.",
                    "category": "Camisetas",
                    "image": "https://via.placeholder.com/300x200/4caf50/ffffff?text=Sudadera+Verde",
                    "size": "L",
                    "color": "Verde",
                    "stock": 35
                }
            ]
            
            for product in sample_products:
                result = self.add_product(product)
                print(f"Producto '{product['name']}': {result['message']}")
            
            return {"success": True, "message": "Datos de muestra creados exitosamente"}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    # Métodos para la base de datos "prueba"
    def get_prueba_products(self):
        """Obtener todos los productos de la base de datos prueba"""
        try:
            # Conectar a la base de datos de prueba
            prueba_db = self.client[DB_NAME_PRUEBA]
            products_collection = prueba_db[COLLECTION_PRUEBA]
            
            # Obtener todos los productos
            products = list(products_collection.find({}))
            
            # Convertir ObjectId a string para JSON serialization
            for product in products:
                if '_id' in product:
                    product['_id'] = str(product['_id'])
            
            return {"success": True, "products": products}
            
        except Exception as e:
            return {"success": False, "message": f"Error obteniendo productos de prueba: {str(e)}"}
    
    def get_prueba_product_by_id(self, product_id):
        """Obtener un producto específico de la base de datos prueba por ID"""
        try:
            from bson import ObjectId
            
            # Conectar a la base de datos de prueba
            prueba_db = self.client[DB_NAME_PRUEBA]
            products_collection = prueba_db[COLLECTION_PRUEBA]
            
            # Buscar producto por ID
            product = products_collection.find_one({"_id": ObjectId(product_id)})
            
            if product:
                # Convertir ObjectId a string
                product['_id'] = str(product['_id'])
                return {"success": True, "product": product}
            else:
                return {"success": False, "message": "Producto no encontrado"}
                
        except Exception as e:
            return {"success": False, "message": f"Error obteniendo producto: {str(e)}"}
    
    def search_prueba_products(self, query):
        """Buscar productos en la base de datos prueba por nombre o tipo"""
        try:
            # Conectar a la base de datos de prueba
            prueba_db = self.client[DB_NAME_PRUEBA]
            products_collection = prueba_db[COLLECTION_PRUEBA]
            
            # Crear query de búsqueda
            search_query = {
                "$or": [
                    {"product_name": {"$regex": query, "$options": "i"}},
                    {"product_type": {"$regex": query, "$options": "i"}}
                ]
            }
            
            # Buscar productos
            products = list(products_collection.find(search_query))
            
            # Convertir ObjectId a string
            for product in products:
                if '_id' in product:
                    product['_id'] = str(product['_id'])
            
            return {"success": True, "products": products}
            
        except Exception as e:
            return {"success": False, "message": f"Error buscando productos: {str(e)}"}
    
    def get_prueba_products_by_type(self, product_type):
        """Obtener productos de la base de datos prueba por tipo"""
        try:
            # Conectar a la base de datos de prueba
            prueba_db = self.client[DB_NAME_PRUEBA]
            products_collection = prueba_db[COLLECTION_PRUEBA]
            
            # Buscar por tipo
            products = list(products_collection.find({"product_type": product_type}))
            
            # Convertir ObjectId a string
            for product in products:
                if '_id' in product:
                    product['_id'] = str(product['_id'])
            
            return {"success": True, "products": products}
            
        except Exception as e:
            return {"success": False, "message": f"Error obteniendo productos por tipo: {str(e)}"}
