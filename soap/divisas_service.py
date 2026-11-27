from wsgiref.simple_server import make_server

from spyne import Application, ServiceBase, Unicode, Array, Fault, Float, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Tasas fijas del PDF: cuantos pesos (MXN) vale 1 unidad de cada moneda.
# Usamos float porque es lo mas simple de manejar en Python (y luego en Java)
# Si luego queremos otra moneda solo se agrega aqui y ya
TASAS = {
    "MXN": 1.0,
    "USD": 18.0,
    "EUR": 21.0,
    "CAD": 13.0,
}


def validar_monedas(origen, destino):
    # Esto lo usan las dos operaciones, asi no repetimos el mismo Fault.
    # Es un error del servicio rechazando la peticion, por eso el codigo es Server
    if origen not in TASAS or destino not in TASAS:
        raise Fault(
            faultcode="Server.MonedaNoSoportada",
            faultstring="Moneda no soportada: %s -> %s" % (origen, destino),
        )



class DivisasService(ServiceBase):

    @rpc(_returns=Array(Unicode))
    def listarMonedas(ctx):
        # las llaves del diccionario son los codigos (MXN, USD...)
        return list(TASAS.keys())

    @rpc(
        Unicode(min_occurs=1, nillable=False),
        Unicode(min_occurs=1, nillable=False),
        _returns=Float,
    )
    def obtenerTipoCambio(ctx, origen, destino):
        validar_monedas(origen, destino)

        # El tipo de cambio es la tasa del destino entre la del origen,
        # asi sale directo de la tabla de tasas
        tipo = TASAS[destino] / TASAS[origen]
        return round(tipo, 6)

    @rpc(
        Float(min_occurs=1, nillable=False),
        Unicode(min_occurs=1, nillable=False),
        Unicode(min_occurs=1, nillable=False),
        _returns=Float,
    )
    def convertir(ctx, monto, origen, destino):
        validar_monedas(origen, destino)

        if monto <= 0:
            raise Fault(
                faultcode="Server.MontoInvalido",
                faultstring=f"El monto debe ser mayor a cero (llego {monto})",
            )

        # Ojo: primero se multiplica y se divide y hasta el final se redondea.
        # Si usaramos el tipo de cambio ya redondeado se arrastra error
        resultado = monto * TASAS[origen] / TASAS[destino]

        # el pdf pide 2 decimales
        return round(resultado, 2)


application = Application(
    [DivisasService],
    tns="http://hotelcolibri.mx/divisas",
    name="Divisas",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_application = WsgiApplication(application)

if __name__ == "__main__":
    server = make_server("0.0.0.0", 8001, wsgi_application)
    print("Servidor escuchando en http://localhost:8001/")
    print("WSDL disponible en http://localhost:8001/?wsdl")
    server.serve_forever()
