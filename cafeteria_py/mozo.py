"""
mozo.py
Representa al mozo que atiende mesas.
Agrega sus propios pedidos (agregación con Pedido).
La clave está encapsulada con name-mangling (__clave).
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido


class Mozo:
    def __init__(self, nombre: str, clave: str):
        self.__nombre: str = nombre
        self.__clave: str = clave          # encapsulado
        self.__pedidos: list[Pedido] = []  # agregación

    #autenticación 
    def verificar_clave(self, intento: str) -> bool:
        return self.__clave == intento

    #propiedades 
    @property
    def nombre(self) -> str:
        return self.__nombre

    #pedidos 
    def agregar_pedido(self, pedido: "Pedido") -> None:
        self.__pedidos.append(pedido)

    @property
    def pedidos(self) -> list["Pedido"]:
        return list(self.__pedidos)

    #totales del día 
    def total_ventas(self) -> float:
        return sum(p.calcular_total() for p in self.__pedidos if p.finalizado)

    def cantidad_pedidos(self) -> int:
        return sum(1 for p in self.__pedidos if p.finalizado)
