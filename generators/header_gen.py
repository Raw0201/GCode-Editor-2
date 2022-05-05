from app_tools.format_tools import *


def header_gen(machine, data) -> list:
    """Generador de líneas de tape

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    if machine in ("B12", "A16"):
        return header_swiss(machine, data)
    elif machine in ("K16", "E16"):
        return header_kswiss(data)
    elif machine in ("HARDINGE", "ROMI"):
        return header_hard_rom(machine, data)
    elif machine == "OMNITURN":
        return header_omni(data)
    elif machine == "MAZAK":
        return header_mazak(data)


def header_swiss(machine: str, data: list) -> list:
    """Encabezado para torno suizo A16 y B12

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch, dia, lgt, chk, cch, wrk = data.values()
    blank_space = fspace()

    num = ftape(mch, prg)
    xin = f"X{fnum3(dia + 0.02)}"
    zin = "Z0" if cch == "DERECHA" else "Z.315"
    chn = "M09" if machine == "A16" else ""
    version = fversion()

    lines1 = [
        "%",
        f"O{num}({prt})",
        f"G50{zin}({mch} - {version})",
        "M06",
        chn,
        "G99M03S7000",
        f"G00{xin}Z-.02M52",
    ]
    lines2 = [blank_space for _ in lines1]
    if not chn:
        del lines2[-1]
    return [lines1, lines2]


def header_kswiss(data: list) -> list:
    """Encabezado para torno suizo K16 y E16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch, dia, lgt, chk, cch, wrk = data.values()
    blank_space = fspace()

    num = ftape(mch, prg)
    xin = f"X{fnum3(dia + 0.02)}"
    zin = "Z0" if cch == "DERECHA" else "Z.44"
    version = fversion()

    lines1 = [
        "%",
        f"O{num}({prt})",
        "$1",
        f"G50{zin}({mch} - {version})",
        "M06",
        "M09",
        "G99M03S7000",
        f"G00{xin}Z-.02M52",
        "G600",
    ]
    lines2 = [
        blank_space,
        blank_space,
        "$2",
        "G50Z0",
        "M89",
        blank_space,
        blank_space,
        blank_space,
        "G600",
    ]
    return [lines1, lines2]


def header_omni(data: list) -> list:
    """Encabezado para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch, dia, lgt, chk, cch, wrk = data.values()
    blank_space = fspace()

    version = fversion()

    lines1 = [f"G90G94F300({prg}  {prt})", f"({mch} - {dsc} - {version})"]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]


def header_mazak(data: list) -> list:
    """Encabezado para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch, dia, lgt, chk, cch, wrk = data.values()
    blank_space = fspace()

    num = ftape(mch, prg)
    version = fversion()

    lines1 = [
        "%",
        f"O{num}({prt})",
        f"({mch} - {dsc} - {version})",
        "G17G20G40G49G80G90G95",
        wrk,
    ]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]


def header_hard_rom(machine: str, data: list) -> list:
    """Encabezado para torno Hardinge

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    prt, prg, dsc, mch, dia, lgt, chk, cch, wrk = data.values()
    blank_space = fspace()

    num = ftape(mch, prg)
    version = fversion()

    lines1 = ["%", f"O{num}({prt})", f"({mch} - {dsc} - {version})"]
    romi = "G20G40G90G95G97"
    hardinge = "G65P9150H1.5G97"

    lines1.append(romi) if machine == "ROMI" else lines1.append(hardinge)
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]
