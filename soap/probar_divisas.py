from zeep import Client
from zeep.exceptions import Fault

# Cliente de prueba para ver cada operacion y cada Fault sin abrir Postman.
# Antes hay que tener corriendo divisas_service.py en otra terminal
client = Client("http://localhost:8001/?wsdl")

print("listarMonedas:", client.service.listarMonedas())

print("\n--- obtenerTipoCambio ---")
for origen, destino in [("USD", "MXN"), ("MXN", "USD"), ("EUR", "CAD"), ("MXN", "JPY")]:
    try:
        r = client.service.obtenerTipoCambio(origen, destino)
        print("obtenerTipoCambio(%s, %s) = %s" % (origen, destino, r))
    except Fault as e:
        print("obtenerTipoCambio(%s, %s) -> Fault %s" % (origen, destino, e.code))

print("\n--- convertir ---")
pruebas = [
    (5400, "MXN", "USD"),   # 300.00
    (5400, "MXN", "EUR"),   # 257.14
    (5400, "MXN", "CAD"),   # 415.38
    (100, "USD", "EUR"),    # 85.71
    (5400, "MXN", "JPY"),   # Fault MonedaNoSoportada
    (0, "MXN", "USD"),      # Fault MontoInvalido
    (-10, "MXN", "USD"),    # Fault MontoInvalido
]

for monto, origen, destino in pruebas:
    try:
        r = client.service.convertir(float(monto), origen, destino)
        print("convertir(%s, %s, %s) = %s" % (monto, origen, destino, r))
    except Fault as e:
        print("convertir(%s, %s, %s) -> Fault %s" % (monto, origen, destino, e.code))
