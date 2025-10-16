#!/usr/bin/env python3
"""
API REST con FastAPI para conectar la aplicación web con MongoDB
Uso: python api_server.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database_manager import DatabaseManager
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tienda de Ropa API", 
    version="1.0.0",
    description="API REST para la tienda de ropa con autenticación y gestión de productos"
)

# Configurar CORS - permite múltiples orígenes para desarrollo y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio de Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

# Modelos Pydantic
class LoginRequest(BaseModel):
    username: str
    password: str

class UserRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "usuario"

class RoleUpdateRequest(BaseModel):
    username: str
    new_role: str

class PermissionCheckRequest(BaseModel):
    username: str
    required_role: str

class ProductRequest(BaseModel):
    name: str
    price: float
    description: str
    category: str
    image: str
    size: str
    color: str
    stock: int = 0

class CartItemRequest(BaseModel):
    product_id: str
    size: str = "M"
    quantity: int = 1

class CartUpdateRequest(BaseModel):
    product_id: str
    size: str
    quantity: int

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a la API de Tienda de Ropa",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    """Verificar que la API está funcionando"""
    logger.info("Health check solicitado")
    return {"status": "OK", "message": "API funcionando correctamente"}

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Autenticar usuario"""
    try:
        logger.info(f"Intento de login para usuario: {request.username}")
        result = db_manager.get_user(request.username, request.password)
        
        if result["success"]:
            logger.info(f"Login exitoso para usuario: {request.username}")
            return {
                "success": True,
                "message": "Login exitoso",
                "user": result["user"]
            }
        else:
            logger.warning(f"Login fallido para usuario: {request.username}")
            raise HTTPException(status_code=401, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/products")
async def get_products():
    """Obtener todos los productos"""
    try:
        logger.info("Solicitando lista de productos")
        result = db_manager.get_all_products()
        
        if result["success"]:
            logger.info(f"Se obtuvieron {len(result['products'])} productos")
            return {
                "success": True,
                "products": result["products"]
            }
        else:
            logger.error(f"Error obteniendo productos: {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """Obtener un producto específico"""
    try:
        result = db_manager.get_all_products()
        
        if result["success"]:
            product = next((p for p in result["products"] if p["id"] == product_id), None)
            if product:
                return {
                    "success": True,
                    "product": product
                }
            else:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.post("/api/users")
async def add_user(request: UserRequest):
    """Agregar nuevo usuario con rol"""
    try:
        result = db_manager.add_user(request.username, request.password, request.role)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.put("/api/users/role")
async def update_user_role(request: RoleUpdateRequest):
    """Actualizar rol de usuario"""
    try:
        result = db_manager.update_user_role(request.username, request.new_role)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/users/role/{role}")
async def get_users_by_role(role: str):
    """Obtener usuarios por rol"""
    try:
        result = db_manager.get_users_by_role(role)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.post("/api/users/permission")
async def check_permission(request: PermissionCheckRequest):
    """Verificar permisos de usuario"""
    try:
        result = db_manager.check_permission(request.username, request.required_role)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/users/roles")
async def get_available_roles():
    """Obtener roles disponibles"""
    return {
        "success": True,
        "roles": [
            {"name": "usuario", "level": 1, "description": "Usuario básico"},
            {"name": "editor", "level": 2, "description": "Puede editar contenido"},
            {"name": "administrador", "level": 3, "description": "Acceso completo"}
        ]
    }

@app.post("/api/products")
async def add_product(request: ProductRequest):
    """Agregar nuevo producto"""
    try:
        logger.info(f"Agregando producto: {request.name}")
        result = db_manager.add_product({
            "name": request.name,
            "price": request.price,
            "description": request.description,
            "category": request.category,
            "image": request.image,
            "size": request.size,
            "color": request.color,
            "stock": request.stock
        })
        return result
        
    except Exception as e:
        logger.error(f"Error agregando producto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.put("/api/products/{product_id}")
async def update_product(product_id: str, request: ProductRequest):
    """Actualizar producto"""
    try:
        logger.info(f"Actualizando producto: {product_id}")
        result = db_manager.update_product(product_id, {
            "name": request.name,
            "price": request.price,
            "description": request.description,
            "category": request.category,
            "image": request.image,
            "size": request.size,
            "color": request.color,
            "stock": request.stock
        })
        return result
        
    except Exception as e:
        logger.error(f"Error actualizando producto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str):
    """Eliminar producto"""
    try:
        logger.info(f"Eliminando producto: {product_id}")
        result = db_manager.delete_product(product_id)
        return result
        
    except Exception as e:
        logger.error(f"Error eliminando producto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

# ==================== ENDPOINTS DEL CARRITO ====================

@app.post("/api/cart/add")
async def add_to_cart(request: CartItemRequest, user_id: str):
    """Agregar producto al carrito del usuario"""
    try:
        logger.info(f"Agregando producto {request.product_id} al carrito del usuario {user_id}")
        result = db_manager.add_to_cart(user_id, request.product_id, request.size, request.quantity)
        return result
        
    except Exception as e:
        logger.error(f"Error agregando al carrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/cart/{user_id}")
async def get_cart(user_id: str):
    """Obtener carrito del usuario"""
    try:
        logger.info(f"Obteniendo carrito del usuario {user_id}")
        result = db_manager.get_cart(user_id)
        return result
        
    except Exception as e:
        logger.error(f"Error obteniendo carrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.put("/api/cart/update")
async def update_cart_item(request: CartUpdateRequest, user_id: str):
    """Actualizar cantidad de un item en el carrito"""
    try:
        logger.info(f"Actualizando item {request.product_id} en carrito del usuario {user_id}")
        result = db_manager.update_cart_item_quantity(
            user_id, 
            request.product_id, 
            request.size, 
            request.quantity
        )
        return result
        
    except Exception as e:
        logger.error(f"Error actualizando carrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.delete("/api/cart/remove")
async def remove_from_cart(request: CartItemRequest, user_id: str):
    """Eliminar producto del carrito"""
    try:
        logger.info(f"Eliminando producto {request.product_id} del carrito del usuario {user_id}")
        result = db_manager.remove_from_cart(user_id, request.product_id, request.size)
        return result
        
    except Exception as e:
        logger.error(f"Error eliminando del carrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.delete("/api/cart/clear/{user_id}")
async def clear_cart(user_id: str):
    """Vaciar carrito del usuario"""
    try:
        logger.info(f"Vaciando carrito del usuario {user_id}")
        result = db_manager.clear_cart(user_id)
        return result
        
    except Exception as e:
        logger.error(f"Error vaciando carrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    print("Iniciando API REST con FastAPI...")
    print("URL: http://localhost:8000")
    print("Documentación: http://localhost:8000/docs")
    print("Endpoints disponibles:")
    print("  POST /api/auth/login - Autenticar usuario")
    print("  GET  /api/products - Obtener productos")
    print("  GET  /api/products/{id} - Obtener producto específico")
    print("  POST /api/users - Agregar usuario")
    print("  GET  /api/health - Verificar estado")
    print("  POST /api/cart/add - Agregar al carrito")
    print("  GET  /api/cart/{user_id} - Obtener carrito")
    print("  PUT  /api/cart/update - Actualizar carrito")
    print("  DELETE /api/cart/remove - Eliminar del carrito")
    print("  DELETE /api/cart/clear/{user_id} - Vaciar carrito")
    print("\nPresiona Ctrl+C para detener el servidor")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
