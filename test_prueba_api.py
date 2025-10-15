#!/usr/bin/env python3
"""
Script para probar la API de productos de la base de datos prueba
"""

import requests
import json

API_BASE_URL = "https://tienda-ropa-api.onrender.com/api"

def test_prueba_endpoints():
    """Probar todos los endpoints de la base de datos prueba"""
    print("🧪 Probando endpoints de la base de datos 'prueba'")
    print("=" * 50)
    
    # 1. Probar obtener todos los productos de prueba
    print("\n1️⃣ Probando GET /prueba/products")
    try:
        response = requests.get(f"{API_BASE_URL}/prueba/products")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {len(data.get('products', []))} productos encontrados")
            if data.get('products'):
                print(f"   Primer producto: {data['products'][0].get('product_name', 'Sin nombre')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 2. Probar búsqueda de productos
    print("\n2️⃣ Probando GET /prueba/search?q=zapatos")
    try:
        response = requests.get(f"{API_BASE_URL}/prueba/search?q=zapatos")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {len(data.get('products', []))} productos encontrados para 'zapatos'")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 3. Probar obtener productos por tipo
    print("\n3️⃣ Probando GET /prueba/products/type/shoes")
    try:
        response = requests.get(f"{API_BASE_URL}/prueba/products/type/shoes")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {len(data.get('products', []))} productos de tipo 'shoes'")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 4. Probar obtener un producto específico (si hay productos)
    print("\n4️⃣ Probando GET /prueba/products/{id}")
    try:
        # Primero obtener la lista para conseguir un ID
        response = requests.get(f"{API_BASE_URL}/prueba/products")
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            if products:
                product_id = products[0].get('_id')
                if product_id:
                    response = requests.get(f"{API_BASE_URL}/prueba/products/{product_id}")
                    if response.status_code == 200:
                        product_data = response.json()
                        print(f"✅ Éxito: Producto encontrado - {product_data.get('product', {}).get('product_name', 'Sin nombre')}")
                    else:
                        print(f"❌ Error: {response.status_code} - {response.text}")
                else:
                    print("⚠️ No se encontró ID de producto para probar")
            else:
                print("⚠️ No hay productos para probar")
        else:
            print(f"❌ Error obteniendo lista de productos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_health():
    """Probar el endpoint de health"""
    print("\n🏥 Probando health check")
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando: {data.get('message', 'OK')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🚀 PRUEBA DE API - BASE DE DATOS PRUEBA")
    print("=" * 50)
    
    test_health()
    test_prueba_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("💡 Si hay errores, verifica que la API esté desplegada en Render.com")
