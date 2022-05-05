from app_tools.format_tools import *
from app_tools.combo_lists import *
from app_tools.compensations_tools import *


def tool_close_gen(machine: str, data: list) -> list:
    """Generador de líneas de tape

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    if machine == "B12":
        return gen_b12(data)
    elif machine == "A16":
        return gen_a16(data)
    elif machine == "K16":
        return gen_k16(data)
    elif machine == "E16":
        return gen_e16(data)
    elif machine == "OMNITURN":
        return gen_omni(data)
    elif machine == "ROMI":
        return gen_romi(data)
    elif machine == "HARDINGE":
        return gen_hardinge(data)
    elif machine == "MAZAK":
        return gen_mazak(data)


def gen_b12(data: list) -> list:
    """Generador de códigos para torno suizo B12

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    xin = f"X{fnum3(dia + .02)}"
    sft = fcom(tol, Compensations.swiss_compensations)
    sft = f"{blk}G50W{fnum3(sft)}" if sft else ""

    if tol in range(21, 34):
        lines1 = [f"{blk}G00Z-.05T00", sft]
    else:
        lines1 = [f"{blk}G00{xin}T00", sft]

    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]
    return [lines1, lines2]


def gen_a16(data: list) -> list:
    """Generador de códigos para torno suizo A16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    xin = f"X{fnum3(dia + .02)}"
    sft = fcom(tol, Compensations.swiss_compensations)
    sft = f"{blk}G50W{fnum3(sft)}" if sft else ""

    if tol in range(21, 34):
        lines1 = [f"{blk}G00Z-.05T00", sft]
    else:
        lines1 = [f"{blk}G00{xin}T00", sft]

    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_k16(data: list) -> list:
    """Generador de códigos para torno suizo K16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    blk = "/" if blk else ""
    xin = f"X{fnum3(dia + .02)}"
    sft = fcom(tol, Compensations.kswiss_compensations)
    sft = f"{blk}G50W{fnum3(sft)}" if sft else ""

    if tol in range(21, 34):
        lines1 = [f"{blk}G00Z-.05T00", sft]
    else:
        lines1 = [f"{blk}G00{xin}T00", sft]

    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_e16(data: list) -> list:
    """Generador de códigos para torno suizo E16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    blk = "/" if blk else ""
    xin = f"X{fnum3(dia + .02)}"
    sft = fcom(tol, Compensations.kswiss_compensations)
    sft = f"{blk}G50W{fnum3(sft)}" if sft else ""

    if tol in range(21, 34):
        lines1 = [f"{blk}G00Z-.05T00", sft]
    else:
        lines1 = [f"{blk}G00{xin}T00", sft]

    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_omni(data: list) -> list:
    """Generador de códigos para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    lines1 = [f"{blk}Z.5F300"]
    lines2 = [blank_space for _ in lines1]

    return [lines1, lines2]


def gen_romi(data: list) -> list:
    """Generador de códigos para torno Romi

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    lines1 = [f"{blk}G00Z.5"]
    lines2 = [blank_space for _ in lines1]

    return [lines1, lines2]


def gen_hardinge(data: list) -> list:
    """Generador de códigos para torno Hardinge

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    lines1 = [f"{blk}G00Z.5"]
    lines2 = [blank_space for _ in lines1]

    return [lines1, lines2]


def gen_mazak(data: list) -> list:
    """Generador de códigos para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    lines1 = [f"{blk}G90G00Z4.0M05M09"]
    lines2 = [blank_space for _ in lines1]

    return [lines1, lines2]
