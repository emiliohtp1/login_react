#!/usr/bin/env python3
"""
Archivo principal para desplegar en Render.com
"""

import os
import uvicorn
from api_server import app

if __name__ == "__main__":
    # Configuración para producción en Render.com
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8000)),
        log_level="info"
    )
