    import itertools

# Esta es tu "Base de Datos" original. Nunca la tocaremos.
productos = {
    1: {"nombre": "papas", "precio": 20},
    2: {"nombre": "refresco", "precio": 15},
    3: {"nombre": "cebolla", "precio": 10},
    4: {"nombre": "galletas", "precio": 13},
    5: {"nombre": "nuez", "precio": 19}
}

def calcular_con_filtro():
    print("--- MENU DEL DÍA ---")
    for id_p, info in productos.items():
        print(f"[{id_p}] {info['nombre']} - ${info['precio']}")

    # 1. Preguntamos qué IDs no están disponibles
    agotados_input = input("\n¿Qué números están agotados? (ejemplo: 1,4 o deja vacío): ")
    
    # Convertimos la entrada en una lista de números
    ids_agotados = []
    if agotados_input.strip():
        ids_agotados = [int(n.strip()) for n in agotados_input.split(",")]

    # 2. EL TRUCO: Creamos una lista 'limpia' usando una "Comprensión de Diccionario"
    # "Crea 'disponibles' usando productos, PERO solo si el ID no está en la lista de agotados"
    disponibles = {id_p: info for id_p, info in productos.items() if id_p not in ids_agotados}

    # 3. Trabajamos SOLO con la lista 'disponibles'
    print(f"\nCalculando solo con: {[item['nombre'] for item in disponibles.values()]}")
    
    try:
        objetivo = float(input("¿Cuánto quieres sumar? $"))
        encontrado = False
        
        items_lista = list(disponibles.values())
        
        for r in range(1, len(items_lista) + 1):
            for combo in itertools.combinations(items_lista, r):
                suma = sum(item['precio'] for item in combo)
                if suma == objetivo:
                    nombres = [item['nombre'] for item in combo]
                    print(f"✔ OPCIÓN: {' + '.join(nombres)} = ${suma}")
                    encontrado = True
        
        if not encontrado:
            print("No hay combinaciones con lo que queda en inventario.")

    except ValueError:
        print("Error: Ingresa un número válido.")

calcular_con_filtro()
