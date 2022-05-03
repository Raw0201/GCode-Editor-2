class Lists:

    machine_list = (
        "B12",
        "A16",
        "K16",
        "E16",
        "MAZAK",
        "OMNITURN",
        "ROMI",
        "HARDINGE",
    )

    tape_sides = ("PRINCIPAL", "SECUNDARIO", "LATERAL")

    cutoff_list = ("DERECHA", "IZQUIERDA", "NO APLICA")

    work_offset_list = (
        "G50 (TORNO)",
        "G54 (PLATO 30 PIEZAS)",
        "G55 (PRENSA PRECISION)",
        "G56 (PRENSA PRECISION)",
        "G57 (APARATO DIVISOR)",
        "G59 (BASE RACKS)",
    )

    tool_list = (
        "CUCHILLA DERECHA",
        "CUCHILLA IZQUIERDA",
        "CUCHILLA TRONZAR",
        "CUCHILLA ROSCAR",
        "CUCHILLA RANURAR",
        "FRESA PLANA",
        "FRESA BOLA",
        "FRESA ESPADA",
        "FRESA CHOCOLA",
        "FRESA ESPECIAL",
        "BROCA PUNTEAR",
        "BROCA",
        "BROCA CENTRO",
        "BROCA ESPECIAL",
        "BARRA TORNEADO",
        "DISCO SIERRA",
        "VOLADOR",
        "RIMA",
        "MACHO ROSCADO",
        "HTA DOBLAR",
        "PIN",
    )

    swiss_compensations = {
        11: 0.06,
        14: 0.1,
        15: 0.03,
        16: 0.295,
        17: 0.295,
        18: 0.295,
    }

    kswiss_compensations = {
        1: 0.06,
        4: 0.1,
        5: 0.03,
        11: 0.394,
        12: 0.394,
        13: 0.394,
        14: 0.394,
    }
