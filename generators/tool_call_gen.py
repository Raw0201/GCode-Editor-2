from app_tools.format_tools import *
from app_tools.combo_lists import *
from app_tools.compensations_tools import *


def tool_call_gen(machine, data) -> list:
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

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    tol = Compensations.kswiss_to_swiss(None, tol, sde)
    data["Tol"] = tol

    sft = fcom(tol, Compensations.swiss_compensations)
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

    return [lines1, lines2]


def gen_a16(data: list) -> list:
    """Generador de códigos para torno suizo A16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    tol = Compensations.kswiss_to_swiss(None, tol, sde)
    data["Tol"] = tol

    sft = fcom(tol, Compensations.swiss_compensations)
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

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_k16(data: list) -> list:
    """Generador de códigos para torno suizo K16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    tol = Compensations.swiss_to_kswiss(None, tol, sde)
    data["Tol"] = tol

    sft = fcom(tol, Compensations.kswiss_compensations)
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

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_e16(data: list) -> list:
    """Generador de códigos para torno suizo E16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    tol = Compensations.swiss_to_kswiss(None, tol, sde)
    data["Tol"] = tol

    sft = fcom(tol, Compensations.kswiss_compensations)
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

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_omni(data: list) -> list:
    """Generador de códigos para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

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


def gen_romi(data: list) -> list:
    """Generador de códigos para torno Romi

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    tol = f"T0{tol}" if tol < 10 else f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    xin = f"X{fnum3(xin)}"
    zin = f"Z{fnum3(zin)}"

    lines1 = [f"{blk}{tol}{tol}G54({typ}{dia}{spc})", f"{blk}G00{xin}{zin}M08"]
    lines2 = [blank_space for _ in lines1]

    return [lines1, lines2]


def gen_hardinge(data: list) -> list:
    """Generador de códigos para torno Hardinge

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    tol = f"T0{tol}" if tol < 10 else f"T{tol}"
    dia = "" if dia == 0 else f" {fdia(dia)}"
    spc = "" if spc == "0" else f" {spc}"
    xin = f"X{fnum3(xin)}"
    zin = f"Z{fnum3(zin)}"

    lines1 = [f"{blk}{tol}({typ}{dia}{spc})", f"{blk}G00{xin}{zin}M08"]
    lines2 = [blank_space for _ in lines1]

    return [lines1, lines2]


def gen_mazak(data: list) -> list:
    """Generador de códigos para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

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
