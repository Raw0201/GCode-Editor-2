class Combo_lists:

    machines = (
        "B12",
        "A16",
        "K16",
        "E16",
        "OMNITURN",
        "ROMI",
        "HARDINGE",
        "MAZAK",
    )

    tape_sides = {
        "PRINCIPAL": "$1",
        "SECUNDARIO": "$2",
        "LATERAL": "$3",
    }

    cutoff_list = (
        "DERECHA",
        "IZQUIERDA",
        "NO APLICA",
    )

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
        "CUCHILLA ESPECIAL",
        "FRESA PLANA",
        "FRESA BOLA",
        "FRESA ESPADA",
        "FRESA CHOCOLA",
        "FRESA ESPECIAL",
        "BROCA PUNTEAR",
        "BROCA",
        "BROCA CENTRO",
        "BROCA ESPECIAL",
        "BARRA TORNEAR",
        "DISCO SIERRA",
        "VOLADOR",
        "RIMA",
        "MACHO ROSCAR",
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

    rotation_directions = (
        "NORMAL",
        "REVERSA",
        "DETENER",
    )

    rotation_commands = {
        "NORMAL1": "M03",
        "REVERSA1": "M04",
        "DETENER1": "M05",
        "NORMAL2": "M23",
        "REVERSA2": "M24",
        "DETENER2": "M25",
        "NORMAL3": "M80",
        "REVERSA3": "M81",
        "DETENER3": "M82",
    }

    program_stops = (
        "",
        "PROGRAMADA",
        "OPCIONAL",
    )

    collet_operations = (
        "",
        "ABRIR",
        "CERRAR",
    )

    coolant_operations = (
        "",
        "ACTIVAR",
        "DESACTIVAR",
    )

    work_planes = (
        "G17(- PLANO X-Y -)",
        "G18(- PLANO X-Z -)",
        "G19(- PLANO Y-Z -)",
    )
