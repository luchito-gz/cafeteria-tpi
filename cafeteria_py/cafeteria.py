"""
cafeteria.py
Clase central del sistema.
Agrega Mozos (agregación 1→N) y administra el menú global.
"""
from producto import Producto, Bebida, Salado, Dulce
from mozo import Mozo


class Cafeteria:
    def __init__(self, clave_gerente: str):
        self.__clave_gerente: str = clave_gerente  # encapsulado
        self.__mozos: list[Mozo] = []              # agregación
        self.__menu: list[Producto] = []
        self.__cargar_menu_inicial()

   

    def verificar_clave_gerente(self, intento: str) -> bool:
        return self.__clave_gerente == intento

    def agregar_producto_al_menu(self, producto: Producto) -> None:
        """Valida que no se duplique nombre+categoría."""
        duplicado = any(
            p.nombre.lower() == producto.nombre.lower()
            and p.categoria == producto.categoria
            for p in self.__menu
        )
        if duplicado:
            raise ValueError("Ya existe ese producto en el menú.")
        self.__menu.append(producto)

    def modificar_precio(self, nombre: str, nuevo_precio: float) -> bool:
        for p in self.__menu:
            if p.nombre.lower() == nombre.lower():
                p.precio = nuevo_precio
                return True
        return False

    def get_cierre_del_dia(self) -> str:
        lineas = [
            "\n" + "=" * 46,
            "            CIERRE DEL DÍA",
            "=" * 46,
        ]
        total_general = 0.0
        for m in self.__mozos:
            lineas.append(
                f"  {m.nombre:<20}  pedidos: {m.cantidad_pedidos():>2}   ${m.total_ventas():>9.2f}"
            )
            total_general += m.total_ventas()
        lineas += [
            "-" * 46,
            f"  TOTAL GENERAL:                   ${total_general:>9.2f}",
            "=" * 46,
        ]
        return "\n".join(lineas)

    

    def registrar_mozo(self, nombre: str, clave: str) -> None:
        if any(m.nombre.lower() == nombre.lower() for m in self.__mozos):
            raise ValueError("Ya existe un mozo con ese nombre.")
        self.__mozos.append(Mozo(nombre, clave))

    def buscar_mozo(self, nombre: str) -> Mozo | None:
        for m in self.__mozos:
            if m.nombre.lower() == nombre.lower():
                return m
        return None

    

    @property
    def menu(self) -> list[Producto]:
        return list(self.__menu)

    def menu_por_categoria(self, categoria: str) -> list[Producto]:
        return [p for p in self.__menu if p.categoria == categoria]


    def __cargar_menu_inicial(self) -> None:
        bebidas = [
            Bebida("Café", 1200.0),
            Bebida("Café con leche", 1500.0),
            Bebida("Té", 1000.0),
            Bebida("Jugo de naranja", 1800.0),
            Bebida("Agua mineral", 800.0),
        ]
        salados = [
            Salado("Medialunas x3", 1400.0),
            Salado("Sándwich jamón y queso", 2500.0),
            Salado("Tostado", 2200.0),
        ]
        dulces = [
            Dulce("Factura", 900.0),
            Dulce("Trozo de torta", 2800.0),
            Dulce("Alfajor", 1100.0),
        ]
        for p in bebidas + salados + dulces:
            self.__menu.append(p)
