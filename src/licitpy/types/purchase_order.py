from enum import Enum


class Status(Enum):
    # ref: https://ayuda.mercadopublico.cl/preguntasfrecuentes/article/KA-01689/es-es
    ACCEPTED = "Aceptada"
    GOODS_RECEIVED = "Recepción Conforme"
    SENT_TO_SUPPLIER = "Enviada a proveedor"
    IN_PROCESS = "En proceso"
