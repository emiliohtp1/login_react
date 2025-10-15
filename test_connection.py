#!/usr/bin/env python3
"""
Script para probar la conexión a MongoDB
Uso: python test_connection.py
"""

from database_manager import DatabaseManager

def main():
    print("🔌 Probando Conexión a MongoDB")
    print("=" * 40)
    
    try:
        # Conectar a la base de datos
        db_manager = DatabaseManager()
        
        # Probar operaciones básicas
        print("📊 Probando operaciones básicas...")
        
        # Listar usuarios
        users_result = db_manager.get_all_users()
        if users_result["success"]:
            print(f"✅ Usuarios encontrados: {len(users_result['users'])}")
            for user in users_result['users']:
                print(f"   👤 {user['username']}")
        else:
            print(f"❌ Error obteniendo usuarios: {users_result['message']}")
        
        # Listar productos
        products_result = db_manager.get_all_products()
        if products_result["success"]:
            print(f"✅ Productos encontrados: {len(products_result['products'])}")
            for product in products_result['products']:
                print(f"   🛍️ {product['name']} - ${product['price']}")
        else:
            print(f"❌ Error obteniendo productos: {products_result['message']}")
        
        print("\n✅ Conexión y operaciones funcionando correctamente")
    
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    finally:
        if 'db_manager' in locals():
            db_manager.disconnect()

if __name__ == "__main__":
    main()
