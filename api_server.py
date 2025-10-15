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
    """Agregar nuevo usuario"""
    try:
        result = db_manager.add_user(request.username, request.password)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

# Endpoints para la base de datos "prueba"
@app.get("/api/prueba/products")
async def get_prueba_products():
    """Obtener todos los productos de la base de datos prueba"""
    try:
        logger.info("Solicitando productos de la base de datos prueba")
        result = db_manager.get_prueba_products()
        
        if result["success"]:
            logger.info(f"Se obtuvieron {len(result['products'])} productos de prueba")
            return {
                "success": True,
                "products": result["products"]
            }
        else:
            logger.error(f"Error obteniendo productos de prueba: {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_prueba_products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/prueba/products/{product_id}")
async def get_prueba_product(product_id: str):
    """Obtener un producto específico de la base de datos prueba"""
    try:
        logger.info(f"Solicitando producto de prueba con ID: {product_id}")
        result = db_manager.get_prueba_product_by_id(product_id)
        
        if result["success"]:
            logger.info("Producto de prueba encontrado")
            return {
                "success": True,
                "product": result["product"]
            }
        else:
            logger.warning(f"Producto de prueba no encontrado: {result['message']}")
            raise HTTPException(status_code=404, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_prueba_product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/prueba/search")
async def search_prueba_products(q: str):
    """Buscar productos en la base de datos prueba"""
    try:
        logger.info(f"Buscando productos de prueba con query: {q}")
        result = db_manager.search_prueba_products(q)
        
        if result["success"]:
            logger.info(f"Se encontraron {len(result['products'])} productos")
            return {
                "success": True,
                "products": result["products"]
            }
        else:
            logger.error(f"Error buscando productos: {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en search_prueba_products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/api/prueba/products/type/{product_type}")
async def get_prueba_products_by_type(product_type: str):
    """Obtener productos de la base de datos prueba por tipo"""
    try:
        logger.info(f"Solicitando productos de prueba por tipo: {product_type}")
        result = db_manager.get_prueba_products_by_type(product_type)
        
        if result["success"]:
            logger.info(f"Se obtuvieron {len(result['products'])} productos del tipo {product_type}")
            return {
                "success": True,
                "products": result["products"]
            }
        else:
            logger.error(f"Error obteniendo productos por tipo: {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_prueba_products_by_type: {str(e)}")
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
    print("\nPresiona Ctrl+C para detener el servidor")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
