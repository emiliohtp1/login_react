from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME, COLLECTION_USERS, COLLECTION_PRODUCTS
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
    
    def add_user(self, username, password, role="usuario"):
        """Agregar un nuevo usuario con rol"""
        try:
            # Verificar si el usuario ya existe
            existing_user = self.db[COLLECTION_USERS].find_one({"username": username})
            if existing_user:
                return {"success": False, "message": "El usuario ya existe"}
            
            # Validar rol
            valid_roles = ["usuario", "editor", "administrador"]
            if role not in valid_roles:
                return {"success": False, "message": f"Rol inválido. Roles válidos: {', '.join(valid_roles)}"}
            
            # Crear nuevo usuario
            user_data = {
                "username": username,
                "password": password,
                "role": role,
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
                        "role": user.get("role", "usuario"),
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
                    "image": "https://picsum.photos/300/200?random=1",
                    "size": "M",
                    "color": "Blanco",
                    "stock": 50
                },
                {
                    "name": "Jeans Clásicos Azules",
                    "price": 59.99,
                    "description": "Jeans de corte clásico en denim azul, cómodos y duraderos.",
                    "category": "Pantalones",
                    "image": "https://picsum.photos/300/200?random=2",
                    "size": "L",
                    "color": "Azul",
                    "stock": 30
                },
                {
                    "name": "Vestido Elegante Negro",
                    "price": 89.99,
                    "description": "Vestido elegante para ocasiones especiales, corte A-line.",
                    "category": "Vestidos",
                    "image": "https://picsum.photos/300/200?random=3",
                    "size": "M",
                    "color": "Negro",
                    "stock": 20
                },
                {
                    "name": "Zapatos Deportivos",
                    "price": 79.99,
                    "description": "Zapatos deportivos cómodos para caminar y hacer ejercicio.",
                    "category": "Zapatos",
                    "image": "https://picsum.photos/300/200?random=4",
                    "size": "42",
                    "color": "Negro",
                    "stock": 25
                },
                {
                    "name": "Collar de Plata",
                    "price": 45.99,
                    "description": "Collar elegante de plata 925, perfecto para complementar cualquier outfit.",
                    "category": "Accesorios",
                    "image": "https://picsum.photos/300/200?random=5",
                    "size": "Único",
                    "color": "Plata",
                    "stock": 15
                },
                {
                    "name": "Sudadera con Capucha",
                    "price": 49.99,
                    "description": "Sudadera cómoda con capucha, ideal para días frescos.",
                    "category": "Camisetas",
                    "image": "https://picsum.photos/300/200?random=6",
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
    
    def delete_product(self, product_id):
        """Eliminar producto por ID"""
        try:
            from bson import ObjectId
            
            # Convertir string ID a ObjectId
            try:
                object_id = ObjectId(product_id)
            except:
                return {"success": False, "message": "ID de producto inválido"}
            
            result = self.db[COLLECTION_PRODUCTS].delete_one({"_id": object_id})
            
            if result.deleted_count > 0:
                return {"success": True, "message": "Producto eliminado exitosamente"}
            else:
                return {"success": False, "message": "Producto no encontrado"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def update_user_role(self, username, new_role):
        """Actualizar el rol de un usuario"""
        try:
            valid_roles = ["usuario", "editor", "administrador"]
            if new_role not in valid_roles:
                return {"success": False, "message": f"Rol inválido. Roles válidos: {', '.join(valid_roles)}"}
            
            result = self.db[COLLECTION_USERS].update_one(
                {"username": username},
                {"$set": {"role": new_role, "updated_at": datetime.now()}}
            )
            
            if result.modified_count > 0:
                return {"success": True, "message": f"Rol de '{username}' actualizado a '{new_role}'"}
            else:
                return {"success": False, "message": "Usuario no encontrado"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_users_by_role(self, role):
        """Obtener usuarios por rol"""
        try:
            valid_roles = ["usuario", "editor", "administrador"]
            if role not in valid_roles:
                return {"success": False, "message": f"Rol inválido. Roles válidos: {', '.join(valid_roles)}"}
            
            users = list(self.db[COLLECTION_USERS].find(
                {"role": role, "is_active": True},
                {"password": 0}  # Excluir contraseñas
            ))
            
            user_list = []
            for user in users:
                user_list.append({
                    "id": str(user["_id"]),
                    "username": user["username"],
                    "role": user.get("role", "usuario"),
                    "created_at": user["created_at"]
                })
            
            return {"success": True, "users": user_list}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def check_permission(self, username, required_role):
        """Verificar si un usuario tiene el rol necesario"""
        try:
            user = self.db[COLLECTION_USERS].find_one(
                {"username": username, "is_active": True},
                {"role": 1}
            )
            
            if not user:
                return {"success": False, "message": "Usuario no encontrado"}
            
            user_role = user.get("role", "usuario")
            
            # Definir jerarquía de roles
            role_hierarchy = {
                "usuario": 1,
                "editor": 2,
                "administrador": 3
            }
            
            user_level = role_hierarchy.get(user_role, 1)
            required_level = role_hierarchy.get(required_role, 1)
            
            if user_level >= required_level:
                return {"success": True, "message": "Permiso concedido"}
            else:
                return {"success": False, "message": f"Permiso denegado. Se requiere rol '{required_role}' o superior"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
