"""
producto.py
Jerarquía de productos del menú.
Aplica: Abstracción, Herencia, Polimorfismo.
"""
from abc import ABC, abstractmethod


class Producto(ABC):
    """Clase abstracta base para todos los productos del menú."""

    def __init__(self, nombre: str, precio: float, categoria: str):
        self._nombre = nombre
        self.__precio = precio          # encapsulado con name-mangling
        self._categoria = categoria

    #getters 
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio(self) -> float:
        return self.__precio

    @property
    def categoria(self) -> str:
        return self._categoria

    #setter con validación 
    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = valor

    #polimorfismo 
    @abstractmethod
    def get_descripcion(self) -> str:
        """Cada subclase resuelve su propia descripción."""
        pass

    def __str__(self) -> str:
        return f"{self.get_descripcion():<30} [{self._categoria:<6}]  ${self.precio:>8.2f}"



class Bebida(Producto):
    def __init__(self, nombre: str, precio: float):
        super().__init__(nombre, precio, "bebida")

    def get_descripcion(self) -> str:
        return self._nombre


class Salado(Producto):
    def __init__(self, nombre: str, precio: float):
        super().__init__(nombre, precio, "salado")

    def get_descripcion(self) -> str:
        return self._nombre


class Dulce(Producto):
    def __init__(self, nombre: str, precio: float):
        super().__init__(nombre, precio, "dulce")

    def get_descripcion(self) -> str:
        return self._nombre
