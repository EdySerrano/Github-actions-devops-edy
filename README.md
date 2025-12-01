### Laboratorio CI/CD DevSecOps con github-actions - [Edy Serrano] - [20211229B]

#### Objetivo del laboratorio

Este proyecto tiene como finalidad implementar un ciclo de vida completo de desarrollo de software seguro (DevSecOps) para una aplicación Python. El flujo comienza con la escritura del código fuente y sus pruebas, seguido de la empaquetación en un contenedor Docker optimizado y seguro. Posteriormente, se ejecuta un pipeline de automatización que integra análisis de seguridad (SAST, SCA, DAST) y generación de SBOM. Finalmente, el artefacto validado se despliega en un clúster de Kubernetes local (KinD), demostrando la integración continua y el despliegue continuo en un entorno controlado.

#### Ejercicio 2 - Workflow de automatización básico

Se ha configurado el workflow `.github/workflows/ci-devsecops.yml` para cumplir con los requisitos de automatización básica:

- **Triggers:** El pipeline se ejecuta automáticamente en `push` y `pull_request` a la rama `main`, y permite ejecución manual (`workflow_dispatch`).
- **Pasos Clave:**
    - Instalación de dependencias desde `requirements-dev.txt`.
    - Construcción de la imagen Docker.
    - Ejecución de pruebas unitarias con `pytest`.
- **Saludo del Pipeline:** Se añadió un paso inicial que imprime información de contexto utilizando variables de GitHub Actions:
    - Repositorio: `${{ github.repository }}`
    - Rama: `${{ github.ref_name }}`

#### Ejercicio 3 - Análisis estático y dependencias

Ya se han integrado herramientas de analisis estático (SAST) y análisis de composición de software (SCA) en el pipeline:

- **Herramientas utilizadas:**
    - **Bandit:** Analisis de seguridad para código Python.
    - **Semgrep:** Analisis estático con reglas personalizadas.
    - **Pip-audit:** Auditoria de vulnerabilidades en dependencias de Python.

- **Configuración de Reglas (Semgrep):**
    - Se ha configurado una regla explícita en `.semgrep.yml` para prohibir el uso de `eval()` y `exec()`, mitigando riesgos de ejecución de código arbitrario.

- **Artefactos generados:**
    - `artifacts/bandit.json`: Reporte de Bandit.
    - `artifacts/semgrep.json`: Reporte de Semgrep.
    - `artifacts/pip-audit.json`: Reporte de auditoría de dependencias.

#### Ejercicio 4 - Imágenes de contenedor y revisión de segurida

##### Análisis de Imagen y Artefactos

El pipeline incluye pasos específicos para la seguridad y trazabilidad de la imagen Docker:

- **Descripción de Componentes (SBOM):** Se utiliza **Syft** para generar un inventario de software (Software Bill of Materials) tanto del proyecto como de la imagen construida.
- **Escaneo de Vulnerabilidades:** Se utiliza **Grype** para analizar la imagen en busca de vulnerabilidades conocidas (CVEs).

**Ubicación de los resultados:**

Los reportes generados se almacenan en el directorio `artifacts/` y se suben como artefactos del workflow:

- `artifacts/sbom-syft-project.json`: SBOM del directorio del proyecto (formato JSON).
- `artifacts/sbom-syft-image.json`: SBOM de la imagen Docker construida (formato JSON).
- `artifacts/grype-image.sarif`: Reporte de vulnerabilidades de la imagen en formato SARIF.

#### Ejercicio 5 - Servicio HTTP, Docker Compose y pruebas de humo

Se ha verificado y mejorado la integración del servicio HTTP y las pruebas automatizadas:

- **Pruebas Unitarias:** Se añadió una nueva prueba `test_root_endpoint` en `tests/test_health.py` que verifica el comportamiento del endpoint raíz `/`, asegurando que devuelve el nombre del servicio correcto y el estado `ok`.
- **Smoke Test en Pipeline:** El workflow ahora levanta el servicio utilizando `docker compose`, espera a que esté listo y realiza una peticion al endpoint `/health`.
- **Visibilidad:** La respuesta JSON del endpoint `/health` se imprime en los logs del pipeline para facilitar la depuración.
- **Limpieza:** Se asegura que los contenedores se detengan y eliminen (`docker compose down -v`) al finalizar el job, independientemente del resultado.
