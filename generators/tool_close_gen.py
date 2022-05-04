from app_tools.format_tools import *
from app_tools.app_lists import *


def tool_close_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    if machine in {"B12", "A16"}:
        return tool_close_swiss(machine, data)
    elif machine in {"K16", "E16"}:
        return tool_close_kswiss(data)
    elif machine in {"HARDINGE", "ROMI"}:
        return tool_close_hard_rom(machine, data)
    elif machine == "OMNITURN":
        return tool_close_omni(data)
    elif machine == "MAZAK":
        return tool_close_mazak(data)


def tool_close_swiss(machine: str, data: list) -> list:
    """Encabezado para torno suizo A16 y B12

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()

    if machine == "B12" and tol in (16, 17, 18):
        return [[blank_space], [blank_space]]

    blk = "/" if blk else ""
    xin = f"X{fnum3(dia + .02)}"
    sft = fcom(tol, Lists.swiss_compensations)
    sft = f"{blk}G50W{fnum3(sft)}" if sft else ""

    if tol in range(21, 34):
        lines1 = [f"{blk}G00Z-.05T00", sft]
    else:
        lines1 = [f"{blk}G00{xin}T00", sft]

    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]
    return [lines2, lines1] if sde == "SECUNDARIO" else [lines1, lines2]


def tool_close_kswiss(data: list) -> list:
    """Encabezado para torno suizo K16 y E16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""
    xin = f"X{fnum3(dia + .02)}"
    sft = fcom(tol, Lists.kswiss_compensations)
    sft = f"{blk}G50W{fnum3(sft)}" if sft else ""

    if tol in range(21, 34):
        lines1 = [f"{blk}G00Z-.05T00", sft]
    else:
        lines1 = [f"{blk}G00{xin}T00", sft]

    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]
    return [lines2, lines1] if sde == "SECUNDARIO" else [lines1, lines2]


def tool_close_omni(data: list) -> list:
    """Encabezado para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""

    lines1 = [f"{blk}Z.5F300"]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]


def tool_close_mazak(data: list) -> list:
    """Encabezado para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""

    lines1 = [f"{blk}G90G00Z4.0M05M09"]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]


def tool_close_hard_rom(machine: str, data: list) -> list:
    """Encabezado para torno Hardinge

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, sde, dia, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""

    lines1 = [f"{blk}G00Z.5"]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]
