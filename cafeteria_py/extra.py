"""
extra.py
Patrón de diseño Decorator para agregar extras a productos.
Extra envuelve un Producto existente, suma precio y extiende la descripción.
"""
from producto import Producto


class Extra(Producto):
    """Decorador abstracto. Hereda de Producto para mantener la misma interfaz."""

    def __init__(self, producto_base: Producto, nombre_extra: str, precio_extra: float):
        # Precio total = base + extra
        super().__init__(
            nombre=producto_base.nombre,
            precio=producto_base.precio + precio_extra,
            categoria=producto_base.categoria,
        )
        self._producto_base = producto_base
        self._nombre_extra = nombre_extra

    def get_descripcion(self) -> str:
        return f"{self._producto_base.get_descripcion()} + {self._nombre_extra}"

    @property
    def nombre_extra(self) -> str:
        return self._nombre_extra



class ExtraLeche(Extra):
    PRECIO = 200.0

    def __init__(self, base: Producto):
        super().__init__(base, "Leche", self.PRECIO)


class ExtraCrema(Extra):
    PRECIO = 300.0

    def __init__(self, base: Producto):
        super().__init__(base, "Crema", self.PRECIO)


class ExtraAzucar(Extra):
    PRECIO = 50.0

    def __init__(self, base: Producto):
        super().__init__(base, "Azúcar", self.PRECIO)
