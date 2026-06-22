"""
pedido.py
Representa un pedido individual de un cliente.
Calcula subtotal, propina y total; genera el ticket imprimible.
"""
from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from producto import Producto

PROPINA = 0.10


class Pedido:
    def __init__(self):
        self.__items: list[Producto] = []
        self.__horario: str = datetime.now().strftime("%H:%M")
        self.__finalizado: bool = False

    #items 
    def agregar_producto(self, producto: "Producto") -> None:
        if self.__finalizado:
            raise RuntimeError("El pedido ya fue cerrado.")
        self.__items.append(producto)

    @property
    def items(self) -> list["Producto"]:
        return list(self.__items)

    @property
    def horario(self) -> str:
        return self.__horario

    @property
    def finalizado(self) -> bool:
        return self.__finalizado

    #cálculos 
    def calcular_subtotal(self) -> float:
        return sum(p.precio for p in self.__items)

    def calcular_propina(self) -> float:
        return self.calcular_subtotal() * PROPINA

    def calcular_total(self) -> float:
        return self.calcular_subtotal() + self.calcular_propina()

    #cierre 
    def finalizar(self) -> None:
        self.__finalizado = True

    #ticket 
    def generar_ticket(self, nombre_mozo: str) -> str:
        lineas = [
            "\n" + "=" * 44,
            "          CAFETERÍA — TICKET",
            "=" * 44,
            f"  Mozo: {nombre_mozo:<20}  {self.__horario}",
            "-" * 44,
        ]
        for p in self.__items:
            lineas.append(f"  {p.get_descripcion():<30}  ${p.precio:>7.2f}")
        lineas += [
            "-" * 44,
            f"  Subtotal:                       ${self.calcular_subtotal():>7.2f}",
            f"  Propina (10%):                  ${self.calcular_propina():>7.2f}",
            "=" * 44,
            f"  TOTAL:                          ${self.calcular_total():>7.2f}",
            "=" * 44,
        ]
        return "\n".join(lineas)
