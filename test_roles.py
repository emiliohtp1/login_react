#!/usr/bin/env python3
"""
Script de prueba para el sistema de roles
Uso: python test_roles.py
"""

import requests
import json
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL de la API (cambiar si es necesario)
API_BASE_URL = "https://tienda-ropa-api.onrender.com/api"

def test_role_system():
    """Probar el sistema de roles completo"""
    
    print("=== PRUEBAS DEL SISTEMA DE ROLES ===")
    print(f"API URL: {API_BASE_URL}")
    print()
    
    # 1. Probar login con diferentes usuarios
    test_users = [
        {"username": "admin@tienda.com", "password": "admin123", "expected_role": "administrador"},
        {"username": "editor@tienda.com", "password": "editor123", "expected_role": "editor"},
        {"username": "usuario@tienda.com", "password": "usuario123", "expected_role": "usuario"}
    ]
    
    print("1. PROBANDO LOGIN CON DIFERENTES ROLES")
    print("-" * 50)
    
    for user in test_users:
        try:
            response = requests.post(f"{API_BASE_URL}/auth/login", json={
                "username": user["username"],
                "password": user["password"]
            })
            
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    actual_role = data["user"].get("role", "sin rol")
                    expected_role = user["expected_role"]
                    
                    if actual_role == expected_role:
                        print(f"✅ {user['username']}: Rol correcto ({actual_role})")
                    else:
                        print(f"❌ {user['username']}: Rol incorrecto. Esperado: {expected_role}, Actual: {actual_role}")
                else:
                    print(f"❌ {user['username']}: Login fallido - {data['message']}")
            else:
                print(f"❌ {user['username']}: Error HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {user['username']}: Error de conexión - {str(e)}")
    
    print()
    
    # 2. Probar obtener usuarios por rol
    print("2. PROBANDO OBTENER USUARIOS POR ROL")
    print("-" * 50)
    
    roles = ["usuario", "editor", "administrador"]
    
    for role in roles:
        try:
            response = requests.get(f"{API_BASE_URL}/users/role/{role}")
            
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    count = len(data["users"])
                    print(f"✅ Rol '{role}': {count} usuarios")
                    for user in data["users"]:
                        print(f"   - {user['username']}")
                else:
                    print(f"❌ Rol '{role}': Error - {data['message']}")
            else:
                print(f"❌ Rol '{role}': Error HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Rol '{role}': Error de conexión - {str(e)}")
    
    print()
    
    # 3. Probar verificación de permisos
    print("3. PROBANDO VERIFICACIÓN DE PERMISOS")
    print("-" * 50)
    
    permission_tests = [
        {"username": "admin@tienda.com", "required_role": "administrador", "should_pass": True},
        {"username": "admin@tienda.com", "required_role": "editor", "should_pass": True},
        {"username": "admin@tienda.com", "required_role": "usuario", "should_pass": True},
        {"username": "editor@tienda.com", "required_role": "administrador", "should_pass": False},
        {"username": "editor@tienda.com", "required_role": "editor", "should_pass": True},
        {"username": "editor@tienda.com", "required_role": "usuario", "should_pass": True},
        {"username": "usuario@tienda.com", "required_role": "administrador", "should_pass": False},
        {"username": "usuario@tienda.com", "required_role": "editor", "should_pass": False},
        {"username": "usuario@tienda.com", "required_role": "usuario", "should_pass": True}
    ]
    
    for test in permission_tests:
        try:
            response = requests.post(f"{API_BASE_URL}/users/permission", json={
                "username": test["username"],
                "required_role": test["required_role"]
            })
            
            if response.status_code == 200:
                data = response.json()
                actual_result = data["success"]
                expected_result = test["should_pass"]
                
                if actual_result == expected_result:
                    status = "✅" if actual_result else "✅"
                    print(f"{status} {test['username']} -> {test['required_role']}: {'Permitido' if actual_result else 'Denegado'}")
                else:
                    print(f"❌ {test['username']} -> {test['required_role']}: Resultado inesperado")
            else:
                print(f"❌ {test['username']} -> {test['required_role']}: Error HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {test['username']} -> {test['required_role']}: Error de conexión - {str(e)}")
    
    print()
    
    # 4. Probar obtener roles disponibles
    print("4. PROBANDO OBTENER ROLES DISPONIBLES")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/users/roles")
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print("✅ Roles disponibles:")
                for role in data["roles"]:
                    print(f"   - {role['name']} (nivel {role['level']}): {role['description']}")
            else:
                print(f"❌ Error obteniendo roles: {data['message']}")
        else:
            print(f"❌ Error HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
    
    print()
    print("=== PRUEBAS COMPLETADAS ===")

if __name__ == "__main__":
    test_role_system()
