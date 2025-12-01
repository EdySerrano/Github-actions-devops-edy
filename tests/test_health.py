import http.client
import os
import subprocess
import time
import json

def test_health_endpoint():
    """
    Prueba de integración mínima del endpoint /health.

    - Levanta el servidor como un subproceso usando `python -m src.app`.
    - Fuerza el puerto 8090 mediante la variable de entorno PORT.
    - Realiza una petición HTTP GET a /health.
    - Verifica que el código de respuesta sea 200.
    - Finalmente detiene el subproceso (servidor).
    """

    print(">> Iniciando prueba del endpoint /health en 127.0.0.1:8090")

    # Copiamos el entorno actual para no perder variables existentes
    env = os.environ.copy()
    env["PORT"] = "8090"
    
    # Inicia el servidor en segundo plano
    proc = subprocess.Popen(
        ["python", "-m", "src.app"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Espera un poco a que levante
        time.sleep(2)
        
        # Hacemos la peticion
        conn = http.client.HTTPConnection("127.0.0.1", 8090, timeout=2)
        conn.request("GET", "/health")
        response = conn.getresponse()
        
        # Verificaciones
        assert response.status == 200, f"El endpoint /health devolvió {response.status}"
        
        data = json.loads(response.read().decode())
        assert data.get("status") == "healthy", "El JSON de respuesta no contiene status: healthy"
        
        print(">> Prueba /health exitosa")
        
    finally:
        # Limpieza: matamos el proceso del servidor
        proc.terminate()
        proc.wait()

def test_root_endpoint():
    """
    Prueba unitaria adicional para el endpoint raíz /.
    Verifica que devuelva el nombre del servicio y ok=True.
    """
    print(">> Iniciando prueba del endpoint / en 127.0.0.1:8091")
    
    env = os.environ.copy()
    env["PORT"] = "8091"
    env["SERVICE_NAME"] = "test-service"
    
    proc = subprocess.Popen(
        ["python", "-m", "src.app"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        time.sleep(2)
        conn = http.client.HTTPConnection("127.0.0.1", 8091, timeout=2)
        conn.request("GET", "/")
        response = conn.getresponse()
        
        assert response.status == 200
        data = json.loads(response.read().decode())
        
        assert data.get("service") == "test-service"
        assert data.get("ok") is True
        
        print(">> Prueba / exitosa")
        
    finally:
        proc.terminate()
        proc.wait()
    # Forzamos el uso del puerto 8090 para esta prueba
    env["PORT"] = "8090"

    # Lanzamos el servidor como subproceso ejecutando el módulo src.app
    print(">> Lanzando servidor como subproceso con 'python -m src.app' en el puerto 8090")
    p = subprocess.Popen(["python", "-m", "src.app"], env=env)

    try:
        # Pequeña espera para darle tiempo al servidor a arrancar
        print(">> Esperando a que el servidor arranque...")
        time.sleep(1.5)

        # Creamos una conexión HTTP hacia localhost:8090
        print(">> Creando conexión HTTP a 127.0.0.1:8090")
        conn = http.client.HTTPConnection("127.0.0.1", 8090, timeout=3)

        # Enviamos petición GET al endpoint /health
        print(">> Enviando petición GET a /health")
        conn.request("GET", "/health")

        # Obtenemos la respuesta del servidor
        resp = conn.getresponse()
        print(f">> Respuesta recibida: status={resp.status}, reason={resp.reason}")

        # Aseguramos que el código de estado sea 200 (OK)
        assert resp.status == 200, f"Se esperaba status 200 y se obtuvo {resp.status}"

        # Cerramos explícitamente la conexión HTTP
        conn.close()
        print(">> Conexión HTTP cerrada correctamente")

    finally:
        # Detenemos el proceso del servidor, incluso si la aserción falla
        print(">> Deteniendo servidor de prueba (subproceso)...")
        p.terminate()
        p.wait(timeout=5)
        print(">> Servidor detenido correctamente")
