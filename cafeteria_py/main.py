"""
main.py
Punto de entrada. Interfaz de consola para Mozo y Gerente.
"""
from cafeteria import Cafeteria
from pedido import Pedido
from producto import Producto
from extra import ExtraLeche, ExtraCrema, ExtraAzucar

cafeteria = Cafeteria(clave_gerente="gerente123")



def leer(prompt: str) -> str:
    return input(prompt).strip()


def leer_float(prompt: str) -> float | None:
    try:
        return float(leer(prompt).replace(",", "."))
    except ValueError:
        print("  Valor inválido.")
        return None


def leer_int(prompt: str) -> int | None:
    try:
        return int(leer(prompt))
    except ValueError:
        print("  Valor inválido.")
        return None




def sesion_mozo() -> None:
    nombre = leer("Nombre del mozo: ")
    clave  = leer("Clave: ")

    mozo = cafeteria.buscar_mozo(nombre)

    if mozo is None:
        confirmacion = leer("Mozo nuevo. Confirme la clave (repita): ")
        if clave != confirmacion:
            print("Las claves no coinciden. Volviendo al inicio.")
            return
        try:
            cafeteria.registrar_mozo(nombre, clave)
            mozo = cafeteria.buscar_mozo(nombre)
            print("  Mozo registrado correctamente.")
        except ValueError as e:
            print(f"  Error: {e}")
            return
    else:
        if not mozo.verificar_clave(clave):
            print("Clave incorrecta.")
            return

    print(f"\n¡Bienvenido, {mozo.nombre}!")

    while True:
        print("\n--- Menú Mozo ---")
        print("  1. Nuevo pedido")
        print("  2. Cerrar sesión")
        op = leer("Opción: ")

        if op == "1":
            nuevo_pedido(mozo)
        elif op == "2":
            break
        else:
            print("Opción inválida.")


def nuevo_pedido(mozo) -> None:
    pedido = Pedido()
    print("\n══ NUEVO PEDIDO ══")

    while True:
        print(f"\n  Subtotal: ${pedido.calcular_subtotal():.2f}  "
              f"| Propina (10%): ${pedido.calcular_propina():.2f}  "
              f"| Total: ${pedido.calcular_total():.2f}")
        print("\n  ¿Qué desea hacer?")
        print("   1. Agregar producto")
        print("   2. Ver pedido actual")
        print("   3. Finalizar y emitir ticket")
        print("   4. Cancelar pedido")
        op = leer("  Opción: ")

        if op == "1":
            agregar_producto(pedido)
        elif op == "2":
            ver_pedido_actual(pedido)
        elif op == "3":
            if not pedido.items:
                print("  El pedido está vacío.")
            else:
                pedido.finalizar()
                mozo.agregar_pedido(pedido)
                print(pedido.generar_ticket(mozo.nombre))
                break
        elif op == "4":
            print("  Pedido cancelado.")
            break
        else:
            print("  Opción inválida.")


def agregar_producto(pedido: Pedido) -> None:
    print("\n  Categorías:")
    print("   1. Bebidas")
    print("   2. Salados")
    print("   3. Dulces")
    op = leer("  Categoría: ")

    categorias = {"1": "bebida", "2": "salado", "3": "dulce"}
    categoria = categorias.get(op)
    if not categoria:
        print("  Categoría inválida.")
        return

    lista = cafeteria.menu_por_categoria(categoria)
    print(f"\n  --- {categoria.upper()}S ---")
    for i, p in enumerate(lista, 1):
        print(f"   {i}. {p}")

    num = leer_int("  Elegir número (0 para cancelar): ")
    if num is None or num == 0:
        return
    if not (1 <= num <= len(lista)):
        print("  Número fuera de rango.")
        return

    elegido: Producto = lista[num - 1]

    if categoria == "bebida":
        elegido = ofrecer_extras(elegido)

    pedido.agregar_producto(elegido)
    print(f"  Agregado: {elegido.get_descripcion()}  ${elegido.precio:.2f}")


def ofrecer_extras(base: Producto) -> Producto:
    while True:
        print(f'\n  Extras para "{base.get_descripcion()}":')
        print(f"   1. Leche   (+${ExtraLeche.PRECIO:.0f})")
        print(f"   2. Crema   (+${ExtraCrema.PRECIO:.0f})")
        print(f"   3. Azúcar  (+${ExtraAzucar.PRECIO:.0f})")
        print("   0. Listo / sin más extras")
        op = leer("  Extra: ")

        if op == "1":
            base = ExtraLeche(base)
        elif op == "2":
            base = ExtraCrema(base)
        elif op == "3":
            base = ExtraAzucar(base)
        elif op == "0":
            break
        else:
            print("  Opción inválida.")
    return base


def ver_pedido_actual(pedido: Pedido) -> None:
    if not pedido.items:
        print("  (pedido vacío)")
        return
    print("\n  Items en el pedido:")
    for p in pedido.items:
        print(f"   · {p.get_descripcion():<32} ${p.precio:.2f}")
    print(f"  Subtotal: ${pedido.calcular_subtotal():.2f}  "
          f"Propina: ${pedido.calcular_propina():.2f}  "
          f"Total: ${pedido.calcular_total():.2f}")




def sesion_gerente() -> None:
    clave = leer("Clave de gerente: ")
    if not cafeteria.verificar_clave_gerente(clave):
        print("Clave incorrecta.")
        return

    print("\n¡Bienvenido, Gerente!")

    while True:
        print("\n--- Menú Gerente ---")
        print("  1. Ver menú completo")
        print("  2. Agregar producto al menú")
        print("  3. Modificar precio de producto")
        print("  4. Ver cierre del día")
        print("  5. Cerrar sesión")
        op = leer("Opción: ")

        if op == "1":
            ver_menu_completo()
        elif op == "2":
            agregar_al_menu()
        elif op == "3":
            modificar_precio()
        elif op == "4":
            print(cafeteria.get_cierre_del_dia())
        elif op == "5":
            break
        else:
            print("Opción inválida.")


def ver_menu_completo() -> None:
    print("\n══ MENÚ ACTUAL ══")
    for cat in ("bebida", "salado", "dulce"):
        print(f"\n  [{cat.upper()}S]")
        for p in cafeteria.menu_por_categoria(cat):
            print(f"   · {p}")


def agregar_al_menu() -> None:
    from producto import Bebida, Salado, Dulce
    print("\n  Categorías: 1=Bebida  2=Salado  3=Dulce")
    op       = leer("  Categoría: ")
    nombre   = leer("  Nombre del producto: ")
    precio   = leer_float("  Precio: $")
    if precio is None:
        return

    clases = {"1": Bebida, "2": Salado, "3": Dulce}
    Clase = clases.get(op)
    if not Clase:
        print("  Categoría inválida.")
        return

    try:
        cafeteria.agregar_producto_al_menu(Clase(nombre, precio))
        print("  Producto agregado.")
    except ValueError as e:
        print(f"  Error: {e}")


def modificar_precio() -> None:
    ver_menu_completo()
    nombre = leer("\n  Nombre del producto a modificar: ")
    precio = leer_float("  Nuevo precio: $")
    if precio is None:
        return

    if cafeteria.modificar_precio(nombre, precio):
        print("  Precio actualizado.")
    else:
        print("  Producto no encontrado.")



def main() -> None:
    print(" SIMULADOR DE PEDIDOS - CAFETERÍA")
    

    while True:
        print("\n¿Quién inicia sesión?")
        print("  1. Mozo")
        print("  2. Gerente")
        print("  3. Salir")
        op = leer("Opción: ")

        if op == "1":
            sesion_mozo()
        elif op == "2":
            sesion_gerente()
        elif op == "3":
            print("\n¡Hasta luego!\n")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
