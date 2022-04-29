from app_tools.format_tools import *


def header_gen(machine, data) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    if machine in ("B12", "A16"):
        return header_swiss(data)
    elif machine in ("K16", "E16"):
        return header_kswiss(data)
    elif machine in ("HARDINGE", "ROMI"):
        return header_hard_rom(data)
    elif machine == "OMNITURN":
        return header_omni(data)
    elif machine == "MAZAK":
        return header_mazak(data)


def header_swiss(data: list) -> list:
    """Encabezado para torno suizo A16 y B12

    Args:
        data (list): Lista de datos de encabezado

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch = data.values()

    num = ftape(mch, prg)

    version = fversion()

    lines1 = ["%", f"O{num}({prt})", f"M06({mch} - {dsc} - {version})"]
    lines2 = [" " for _ in lines1]
    return [lines1, lines2]


def header_kswiss(data: list) -> list:
    """Encabezado para torno suizo K16 y E16

    Args:
        data (list): Lista de datos de encabezado

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch = data.values()

    num = ftape(mch, prg)
    version = fversion()

    lines1 = ["%", f"O{num}({prt})", F"$1({mch} - {dsc} - {version})"]
    lines2 = ["$2(PROGRAMA SECUNDARIO)", "M89", "G50Z0"]
    return [lines1, lines2]


def header_omni(data: list) -> list:
    """Encabezado para torno OmniTurn

    Args:
        data (list): Lista de datos de encabezado

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch = data.values()

    version = fversion()

    lines1 = [f"G90G94F300({prg}  {prt})", f"({mch} - {dsc} - {version})"]
    lines2 = [" " for _ in lines1]
    return [lines1, lines2]


def header_mazak(data: list) -> list:
    """Encabezado para fresadora Mazak

    Args:
        data (list): Lista de datos de encabezado

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch = data.values()

    num = ftape(mch, prg)
    version = fversion()

    lines1 = ["%", f"O{num}({prt})", f"({mch} - {dsc} - {version})"]
    lines2 = [" " for _ in lines1]
    return [lines1, lines2]


def header_hard_rom(data: list) -> list:
    """Encabezado para torno Hardinge

    Args:
        data (list): Lista de datos de encabezado

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch = data.values()

    num = ftape(mch, prg)
    version = fversion()

    lines1 = ["%", f"O{num}({prt})", f"({mch} - {dsc} - {version})"]
    lines2 = [" " for _ in lines1]
    return [lines1, lines2]
