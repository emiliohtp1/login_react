#!/usr/bin/env python3
"""
Script para agregar usuarios a la base de datos MongoDB
Uso: python add_user.py
"""

from database_manager import DatabaseManager
import getpass

def main():
    print("🔐 Agregar Usuario a la Base de Datos")
    print("=" * 40)
    
    # Conectar a la base de datos
    db_manager = DatabaseManager()
    
    try:
        # Solicitar datos del usuario
        username = input("👤 Ingresa el nombre de usuario (email): ").strip()
        if not username:
            print("❌ El nombre de usuario no puede estar vacío")
            return
        
        password = getpass.getpass("🔒 Ingresa la contraseña: ").strip()
        if not password:
            print("❌ La contraseña no puede estar vacía")
            return
        
        # Confirmar contraseña
        confirm_password = getpass.getpass("🔒 Confirma la contraseña: ").strip()
        if password != confirm_password:
            print("❌ Las contraseñas no coinciden")
            return
        
        # Solicitar rol
        print("\n👥 Roles disponibles:")
        print("1. usuario (básico)")
        print("2. editor (puede editar contenido)")
        print("3. administrador (acceso completo)")
        
        role_choice = input("🎭 Selecciona el rol (1-3) [1]: ").strip()
        
        role_map = {
            "1": "usuario",
            "2": "editor", 
            "3": "administrador"
        }
        
        role = role_map.get(role_choice, "usuario")
        print(f"🎭 Rol seleccionado: {role}")
        
        # Agregar usuario
        print("\n⏳ Agregando usuario...")
        result = db_manager.add_user(username, password, role)
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"🆔 ID del usuario: {result['user_id']}")
        else:
            print(f"❌ {result['message']}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main()
