#!/usr/bin/env python3
"""
Script para migrar usuarios existentes y agregar el campo de rol
Uso: python migrate_roles.py
"""

from database_manager import DatabaseManager
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def migrate_users_to_roles():
    """Migrar usuarios existentes para incluir roles"""
    try:
        db_manager = DatabaseManager()
        
        # Obtener todos los usuarios sin rol
        users_without_role = list(db_manager.db[db_manager.COLLECTION_USERS].find(
            {"role": {"$exists": False}}
        ))
        
        logger.info(f"Encontrados {len(users_without_role)} usuarios sin rol")
        
        # Asignar rol "usuario" por defecto a usuarios existentes
        for user in users_without_role:
            result = db_manager.db[db_manager.COLLECTION_USERS].update_one(
                {"_id": user["_id"]},
                {"$set": {"role": "usuario"}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Usuario '{user['username']}' actualizado con rol 'usuario'")
            else:
                logger.warning(f"No se pudo actualizar usuario '{user['username']}'")
        
        # Crear usuarios de ejemplo con diferentes roles
        sample_users = [
            {"username": "admin@tienda.com", "password": "admin123", "role": "administrador"},
            {"username": "editor@tienda.com", "password": "editor123", "role": "editor"},
            {"username": "usuario@tienda.com", "password": "usuario123", "role": "usuario"}
        ]
        
        logger.info("Creando usuarios de ejemplo con diferentes roles...")
        
        for user_data in sample_users:
            # Verificar si el usuario ya existe
            existing_user = db_manager.db[db_manager.COLLECTION_USERS].find_one(
                {"username": user_data["username"]}
            )
            
            if not existing_user:
                result = db_manager.add_user(
                    user_data["username"], 
                    user_data["password"], 
                    user_data["role"]
                )
                logger.info(f"Usuario '{user_data['username']}' creado: {result['message']}")
            else:
                # Actualizar rol si ya existe
                result = db_manager.update_user_role(
                    user_data["username"], 
                    user_data["role"]
                )
                logger.info(f"Usuario '{user_data['username']}' actualizado: {result['message']}")
        
        # Mostrar resumen de usuarios por rol
        logger.info("\n=== RESUMEN DE USUARIOS POR ROL ===")
        
        for role in ["usuario", "editor", "administrador"]:
            result = db_manager.get_users_by_role(role)
            if result["success"]:
                count = len(result["users"])
                logger.info(f"{role.capitalize()}: {count} usuarios")
                for user in result["users"]:
                    logger.info(f"  - {user['username']}")
            else:
                logger.error(f"Error obteniendo usuarios de rol '{role}': {result['message']}")
        
        logger.info("\nMigración completada exitosamente!")
        
    except Exception as e:
        logger.error(f"Error durante la migración: {str(e)}")
        raise e
    finally:
        if 'db_manager' in locals():
            db_manager.disconnect()

if __name__ == "__main__":
    print("=== MIGRACIÓN DE ROLES DE USUARIOS ===")
    print("Este script migrará usuarios existentes y creará usuarios de ejemplo")
    print("con diferentes roles: usuario, editor, administrador")
    print()
    
    try:
        migrate_users_to_roles()
        print("\n✅ Migración completada exitosamente!")
        print("\nUsuarios de ejemplo creados:")
        print("- admin@tienda.com / admin123 (administrador)")
        print("- editor@tienda.com / editor123 (editor)")
        print("- usuario@tienda.com / usuario123 (usuario)")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {str(e)}")
        print("Verifica la conexión a MongoDB y las credenciales")
