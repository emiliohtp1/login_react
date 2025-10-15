#!/usr/bin/env python3
"""
Script simple para iniciar la API con FastAPI
"""

import uvicorn
from api_server import app

if __name__ == "__main__":
    print("Iniciando API REST con FastAPI...")
    print("URL: http://localhost:8000")
    print("Documentación: http://localhost:8000/docs")
    print("\nPresiona Ctrl+C para detener el servidor")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
