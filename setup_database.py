#!/usr/bin/env python3
"""
Script para configurar la base de datos con datos iniciales
Uso: python setup_database.py
"""

from database_manager import DatabaseManager

def main():
    print("Configuracion de Base de Datos")
    print("=" * 40)
    
    # Conectar a la base de datos
    db_manager = DatabaseManager()
    
    try:
        print("Creando datos de muestra...")
        result = db_manager.create_sample_data()
        
        if result["success"]:
            print(f"OK: {result['message']}")
            print("\nResumen de datos creados:")
            print("Usuario admin: admin@tienda.com / admin123")
            print("6 productos de muestra en diferentes categorias")
        else:
            print(f"Error: {result['message']}")
    
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main()
