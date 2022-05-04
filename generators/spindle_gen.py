from app_tools.format_tools import *


def spindle_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    if machine in {"B12", "A16"}:
        return spindle_swiss(machine, data)
    elif machine in {"K16", "E16"}:
        return spindle_kswiss(machine, data)
    elif machine in {"HARDINGE", "ROMI"}:
        return spindle_hard_rom(machine, data)
    elif machine == "OMNITURN":
        return spindle_omni(data)
    elif machine == "MAZAK":
        return spindle_mazak(data)


def spindle_swiss(machine: str, data: list) -> list:
    """Encabezado para torno suizo A16 y B12

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    spd, rot, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""

    if spd == 0 and rot != "DETENER":
        if sde == "PRINCIPAL":
            return [[f"{blk}G98"], [blank_space]]
        else:
            return [[blank_space], [blank_space]]

    spindle = Lists.tape_sides[sde]

    spd = f"S{spd}" if rot in ("NORMAL", "REVERSA") else ""
    rot = f"{rot}{spindle}"
    rot = Lists.rotation_commands[rot]
    line = f"{blk}{rot}{spd}"

    lines1 = (
        [blank_space] if machine == "B12" and sde != "PRINCIPAL" else [line]
    )
    lines2 = [blank_space]

    return [lines2, lines1] if sde == "SECUNDARIO" else [lines1, lines2]


def spindle_kswiss(machine: str, data: list) -> list:
    """Encabezado para torno suizo A16 y B12

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    spd, rot, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""

    if spd == 0 and rot != "DETENER":
        if sde == "PRINCIPAL":
            return [[f"{blk}G98"], [blank_space]]
        else:
            return [[blank_space], [blank_space]]

    spindle = Lists.tape_sides[sde]

    pfx = f"S{spindle}=" if machine == "E16" else "S"
    spd = f"{pfx}{spd}" if rot in ("NORMAL", "REVERSA") else ""

    rot = f"{rot}{spindle}"
    rot = Lists.rotation_commands[rot]
    line = f"{blk}{rot}{spd}"

    lines1 = [line]
    lines2 = [blank_space]

    return [lines2, lines1] if sde == "SECUNDARIO" else [lines1, lines2]


def spindle_omni(data: list) -> list:
    """Encabezado para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    spd, rot, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""

    if spd == 0 and rot != "DETENER":
        if sde == "PRINCIPAL":
            return [[f"{blk}G94"], [blank_space]]
        else:
            return [[blank_space], [blank_space]]

    spindle = Lists.tape_sides[sde]

    spd = f"S{spd}" if rot in ("NORMAL", "REVERSA") else ""

    rot = f"{rot}{spindle}"
    rot = Lists.rotation_commands[rot]
    line = f"{blk}{rot}{spd}"

    lines1 = [blank_space] if sde != "PRINCIPAL" else [line]
    lines2 = [blank_space]

    return [lines1, lines2]


def spindle_mazak(data: list) -> list:
    """Encabezado para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    spd, rot, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""

    if spd == 0 and rot != "DETENER":
        if sde == "PRINCIPAL":
            return [[f"{blk}G94"], [blank_space]]
        else:
            return [[blank_space], [blank_space]]

    spindle = Lists.tape_sides[sde]

    spd = f"S{spd}" if rot in ("NORMAL", "REVERSA") else ""

    rot = f"{rot}{spindle}"
    rot = Lists.rotation_commands[rot]
    line = f"{blk}{rot}{spd}"

    lines1 = [blank_space] if sde != "PRINCIPAL" else [line]
    lines2 = [blank_space]

    return [lines1, lines2]


def spindle_hard_rom(machine: str, data: list) -> list:
    """Encabezado para torno Hardinge

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    spd, rot, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""

    if spd == 0 and rot != "DETENER":
        if sde != "PRINCIPAL":
            return [[blank_space], [blank_space]]

        cmd = "G94" if machine == "ROMI" else "G95"
        return [[f"{blk}{cmd}"], [blank_space]]

    spindle = Lists.tape_sides[sde]

    spd = f"S{spd}" if rot in ("NORMAL", "REVERSA") else ""
    rot = f"{rot}{spindle}"
    rot = Lists.rotation_commands[rot]
    rot = f"{rot}{spd}"

    cmd = "G95" if machine == "ROMI" else "G99"
    cmd = "" if rot == "M05" else cmd

    lines1 = [f"{blk}{cmd}{rot}"]
    lines2 = [blank_space]

    return [lines1, lines2] if sde == "PRINCIPAL" else [lines2, lines2]
