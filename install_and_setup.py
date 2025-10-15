#!/usr/bin/env python3
"""
Script de instalación y configuración automática
Uso: python install_and_setup.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return False

def main():
    print("🚀 Instalación y Configuración de Base de Datos")
    print("=" * 50)
    
    # Verificar si pip está disponible
    if not run_command("pip --version", "Verificando pip"):
        print("❌ pip no está disponible. Instala Python con pip primero.")
        return
    
    # Instalar dependencias
    if not run_command("pip install -r requirements.txt", "Instalando dependencias"):
        print("❌ Error instalando dependencias")
        return
    
    # Probar conexión
    print("\n🔌 Probando conexión a MongoDB...")
    try:
        from database_manager import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.disconnect()
        print("✅ Conexión a MongoDB exitosa")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        print("💡 Verifica que las credenciales en config.py sean correctas")
        return
    
    # Configurar datos iniciales
    print("\n📊 Configurando datos iniciales...")
    if not run_command("python setup_database.py", "Creando datos de muestra"):
        print("❌ Error configurando datos iniciales")
        return
    
    print("\n🎉 ¡Configuración completada exitosamente!")
    print("\n📋 Resumen:")
    print("✅ Dependencias instaladas")
    print("✅ Conexión a MongoDB verificada")
    print("✅ Datos de muestra creados")
    print("\n🔐 Usuario por defecto:")
    print("   Email: admin@tienda.com")
    print("   Contraseña: admin123")
    print("\n🚀 La aplicación web ya puede usar la base de datos real")

if __name__ == "__main__":
    main()
