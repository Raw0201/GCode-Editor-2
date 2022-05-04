from app_tools.format_tools import *
from app_tools.app_lists import *


def tool_call_gen(machine, data) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    if machine in {"B12", "A16"}:
        return tool_call_swiss(machine, data)
    elif machine in {"K16", "E16"}:
        return tool_call_kswiss(data)
    elif machine in {"HARDINGE", "ROMI"}:
        return tool_call_hard_rom(machine, data)
    elif machine == "OMNITURN":
        return tool_call_omni(data)
    elif machine == "MAZAK":
        return tool_call_mazak(data)


def tool_call_swiss(machine: str, data: list) -> list:
    """Encabezado para torno suizo A16 y B12

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()

    tol = kswiss_to_swiss(tol, sde)
    data["Tol"] = tol

    if machine == "B12" and tol in (16, 17, 18):
        return [[blank_space], [blank_space]]

    blk = "/" if blk else ""
    sft = fcom(tol, Lists.swiss_compensations)
    sft = f"{blk}G50W-{fnum3(sft)}" if sft else ""
    tol = f"T0{tol}" if tol < 10 else f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    zin = f"Z{fnum3(zin)}"

    lines1 = [
        f"{blk}{tol}00({typ}{dia}{spc})",
        sft,
        f"{blk}G00{zin}{tol}",
    ]
    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]

    return [lines2, lines1] if sde == "SECUNDARIO" else [lines1, lines2]


def tool_call_kswiss(data: list) -> list:
    """Encabezado para torno suizo K16 y E16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()

    tol = swiss_to_kswiss(tol, sde)
    data["Tol"] = tol

    blk = "/" if blk else ""
    sft = fcom(tol, Lists.kswiss_compensations)
    sft = f"{blk}G50W-{fnum3(sft)}" if sft else ""
    tol = f"T0{tol}" if tol < 10 else f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    zin = f"Z{fnum3(zin)}"

    lines1 = [
        f"{blk}{tol}00({typ}{dia}{spc})",
        sft,
        f"{blk}G00{zin}{tol}",
    ]
    lines2 = [blank_space for _ in lines1]
    if not sft:
        del lines2[-1]

    return [lines2, lines1] if sde == "SECUNDARIO" else [lines1, lines2]


def tool_call_omni(data: list) -> list:
    """Encabezado para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""
    tol = f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    xin = f"X{fnum3(xin)}"
    zin = f"Z{fnum3(zin)}"

    lines1 = [
        f"{blk}{tol}({typ}{dia}{spc})",
        f"{blk}{xin}{zin}",
    ]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]


def tool_call_mazak(data: list) -> list:
    """Encabezado para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""
    tol = f"T0{tol}" if tol < 10 else f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    xin = f"X{fnum3(xin)}"
    yin = f"Y{fnum3(yin)}"
    zin = f"Z{fnum3(zin)}"

    lines1 = [
        f"{blk}{tol}T00M06({typ}{dia}{spc})",
        f"{blk}G90G00{xin}{yin}{zin}",
    ]
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]


def tool_call_hard_rom(machine: str, data: list) -> list:
    """Encabezado para torno Hardinge

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""
    tol = f"T0{tol}" if tol < 10 else f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    xin = f"X{fnum3(xin)}"
    zin = f"Z{fnum3(zin)}"

    romi = [f"{blk}{tol}{tol}G54({typ}{dia}{spc})", f"{blk}G00{xin}{zin}M08"]
    hardinge = [f"{blk}{tol}({typ}{dia}{spc})", f"{blk}G00{xin}{zin}M08"]

    lines1 = romi if machine == "ROMI" else hardinge
    lines2 = [blank_space for _ in lines1]
    return [lines1, lines2]
