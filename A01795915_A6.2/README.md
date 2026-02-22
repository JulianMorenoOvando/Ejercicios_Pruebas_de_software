# A01795915_A6.2
## Sistema de Reservación de Hoteles - Pruebas de Software y Aseguramiento de la Calidad

## Autores
- Julian Jesús Moreno Ovando
- A01795915 

## Fecha
- 2026-02-21

## Requisitos
- Python 3.11+
- pytest (Para ejecutar las pruebas unitarias)
- pylint / flake8 (Para auditoría de código)

## Ejecución
- Es necesario entrar a la carpeta del proyecto y ejecutar los archivos desde la terminal.
- El sistema cuenta con tres pruebas o demostraciones principales ubicadas en la carpeta `source`:
  1. `test_demo.py`: Una demostración de ejecución del sistema en consola.
  2. `test_classes.py`: Archivo de pruebas unitarias.
  3. `test_pep8.py`: Archivo de comprobación de calidad de código.

## Ejemplo de ejecución
- `cd A01795915_A6.2/`
- **Para ejecutar la demostración:**
  `python source/test_demo.py`
- **Para ejecutar las pruebas unitarias usando pytest:**
  `pytest source/test_classes.py`
  *(Alternativamente: `python -m unittest source/test_classes.py`)*
- **Para ejecutar las pruebas de control de estilo (PEP8):**
  `python source/test_pep8.py`

## Salida
- Las pruebas y los scripts de demostración mostrarán los resultados y el paso a paso en su misma terminal de comandos.
- Los datos de demostración y reservaciones son persistentes y se guardarán como archivos JSON en la carpeta `tests/`.

## Auditoría
- Se anexa la compatibilidad del código validada bajo los estándares PEP8 utilizando las herramientas Pylint y Flake8.

## Nota
- Asegúrese de estar dentro del directorio `A01795915_A6.2` para que las rutas de los archivos generados funcionen correctamente.
