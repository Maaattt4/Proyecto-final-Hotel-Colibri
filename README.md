# Hotel Colibrí – Proyecto final SOA

Sistema de reservas con dos servicios SOAP (Python + spyne) y una API REST (Java 21, Spring Boot, MySQL).

## Integrantes

- Gibran de Jesus Razo Toledo
- Jorge Alberto Mompin Gonzalez
- Genesis Mariana Aguilar Teran

## Estado del proyecto

| Avance | Contenido | Estado |
|---|---|---|
| 1 · Diseño | Borrador de documento y servicio de divisas con WSDL | Hecho (`docs/borrador_arquitectura.md`, `soap/divisas_service.py`) |
| 2 · Demostración | Servicios SOAP + API con habitaciones, reservas y cotización | Pendiente |
| Final | Repositorio completo, documento, Postman y evidencias | Pendiente |

## Requisitos

- Python 3 con `venv` y Git (para instalar spyne desde GitHub).
- Java 21 y MySQL (se usarán desde el Avance 2).

> El enunciado pide Python 3.11. Con Python 3.12 o posterior, `spyne 2.14` (PyPI) no se puede importar, así que `requirements.txt` instala el commit de GitHub `2.15.0a0`, el mismo que usamos en las actividades.

## Cómo arrancar el servicio de divisas

```powershell
cd soap
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe divisas_service.py
```

- Servicio: `http://localhost:8001/`
- WSDL: `http://localhost:8001/?wsdl` (copia en `docs/wsdl/divisas.wsdl`)

## Cómo probarlo

Con el servicio corriendo, en otra terminal:

```powershell
cd soap
.venv\Scripts\python.exe probar_divisas.py
```

Resultados esperados según el enunciado: 5,400 MXN → 300.00 USD, 257.14 EUR, 415.38 CAD; moneda `JPY` → `Client.MonedaNoSoportada`; monto 0 → `Client.MontoInvalido`.


## Uso de inteligencia artificial

Usamos Claude y Gemini como apoyo para la documentación, para resolver dudas, para funciones concretas, para pedir ideas y darle forma al proyecto, y como ayuda y guía para elaborar el código.


