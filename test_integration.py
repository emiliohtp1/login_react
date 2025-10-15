#!/usr/bin/env python3
"""
Script para probar la integración completa con la aplicación React Native
Uso: python test_integration.py
"""

from database_manager import DatabaseManager
import json

def test_user_authentication():
    """Probar autenticación de usuarios"""
    print("🔐 Probando Autenticación de Usuarios")
    print("-" * 40)
    
    db_manager = DatabaseManager()
    
    try:
        # Probar credenciales correctas
        print("✅ Probando credenciales correctas...")
        result = db_manager.get_user("admin@tienda.com", "admin123")
        if result["success"]:
            print(f"   ✅ Login exitoso: {result['user']['username']}")
        else:
            print(f"   ❌ Error: {result['message']}")
        
        # Probar credenciales incorrectas
        print("❌ Probando credenciales incorrectas...")
        result = db_manager.get_user("admin@tienda.com", "wrongpassword")
        if not result["success"]:
            print(f"   ✅ Correctamente rechazado: {result['message']}")
        else:
            print("   ❌ Error: Debería haber rechazado credenciales incorrectas")
        
        # Probar usuario inexistente
        print("👤 Probando usuario inexistente...")
        result = db_manager.get_user("nonexistent@test.com", "password")
        if not result["success"]:
            print(f"   ✅ Correctamente rechazado: {result['message']}")
        else:
            print("   ❌ Error: Debería haber rechazado usuario inexistente")
    
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
    finally:
        db_manager.disconnect()

def test_products():
    """Probar obtención de productos"""
    print("\n🛍️ Probando Productos")
    print("-" * 40)
    
    db_manager = DatabaseManager()
    
    try:
        result = db_manager.get_all_products()
        if result["success"]:
            print(f"✅ Productos obtenidos: {len(result['products'])}")
            for product in result['products'][:3]:  # Mostrar solo los primeros 3
                print(f"   🛍️ {product['name']} - ${product['price']} ({product['category']})")
            if len(result['products']) > 3:
                print(f"   ... y {len(result['products']) - 3} más")
        else:
            print(f"❌ Error obteniendo productos: {result['message']}")
    
    except Exception as e:
        print(f"❌ Error en productos: {e}")
    finally:
        db_manager.disconnect()

def test_add_user():
    """Probar agregar usuario"""
    print("\n👤 Probando Agregar Usuario")
    print("-" * 40)
    
    db_manager = DatabaseManager()
    
    try:
        # Agregar usuario de prueba
        test_username = "test@example.com"
        test_password = "test123"
        
        result = db_manager.add_user(test_username, test_password)
        if result["success"]:
            print(f"✅ Usuario agregado: {result['message']}")
            
            # Verificar que se puede autenticar
            auth_result = db_manager.get_user(test_username, test_password)
            if auth_result["success"]:
                print("✅ Usuario se puede autenticar correctamente")
            else:
                print(f"❌ Error autenticando usuario recién creado: {auth_result['message']}")
        else:
            print(f"❌ Error agregando usuario: {result['message']}")
    
    except Exception as e:
        print(f"❌ Error agregando usuario: {e}")
    finally:
        db_manager.disconnect()

def main():
    print("🧪 Prueba de Integración Completa")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    test_user_authentication()
    test_products()
    test_add_user()
    
    print("\n🎉 ¡Pruebas de integración completadas!")
    print("\n💡 La base de datos está lista para ser usada por la aplicación React Native")

if __name__ == "__main__":
    main()
