from app_tools.format_tools import *
from app_tools.cnc_codes import *
from app_tools.combo_lists import *


def misc_gen(machine: str, data: list) -> list:
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

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    com = "" if com == "" else f"(- {com} -)"
    stp = Swiss_lathe.m_codes[f"PARADA {stp}"]
    chk = Swiss_lathe.m_codes[f"{chk} BOQUILLA"]
    col = Swiss_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines1, lines2]


def gen_a16(data: list) -> list:
    """Generador de códigos para torno suizo A16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    com = "" if com == "" else f"(- {com} -)"
    stp = Swiss_k_lathe.m_codes[f"PARADA {stp}"]
    chk = Swiss_k_lathe.m_codes[f"{chk} BOQUILLA {sde}"]
    col = Swiss_k_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_k16(data: list) -> list:
    """Generador de códigos para torno suizo K16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    com = "" if com == "" else f"(- {com} -)"
    stp = Swiss_k_lathe.m_codes[f"PARADA {stp}"]
    chk = Swiss_k_lathe.m_codes[f"{chk} BOQUILLA {sde}"]
    col = Swiss_k_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_e16(data: list) -> list:
    """Generador de códigos para torno suizo E16

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    com = "" if com == "" else f"(- {com} -)"
    stp = Swiss_k_lathe.m_codes[f"PARADA {stp}"]
    chk = Swiss_k_lathe.m_codes[f"{chk} BOQUILLA {sde}"]
    col = Swiss_k_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines2, lines1] if sde == "$2" else [lines1, lines2]


def gen_omni(data: list) -> list:
    """Generador de códigos para torno OmniTurn

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    com = "" if com == "" else f"(- {com} -)"
    stp = Omni_lathe.m_codes[f"PARADA {stp}"]
    chk = Omni_lathe.m_codes[f"{chk} BOQUILLA"]
    col = Omni_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines1, lines2]


def gen_romi(data: list) -> list:
    """Generador de códigos para torno Romi

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    com = "" if com == "" else f"(- {com} -)"
    stp = Romi_lathe.m_codes[f"PARADA {stp}"]
    chk = Romi_lathe.m_codes[f"{chk} BOQUILLA"]
    col = Romi_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines1, lines2]


def gen_hardinge(data: list) -> list:
    """Generador de códigos para torno Hardinge

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    com = "" if com == "" else f"(- {com} -)"
    stp = Hardinge_lathe.m_codes[f"PARADA {stp}"]
    chk = Hardinge_lathe.m_codes[f"{chk} BOQUILLA"]
    col = Hardinge_lathe.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines1, lines2]


def gen_mazak(data: list) -> list:
    """Generador de códigos para fresadora Mazak

    Args:
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape generadas
    """

    com, stp, chk, col, sde, blk = data.values()
    blank_space = fspace()
    blk = "/" if blk else ""
    sde = Combo_lists.tape_sides[sde]

    if sde != "$1":
        return [[blank_space], [blank_space]]

    com = "" if com == "" else f"(- {com} -)"
    stp = Mazak_mill.m_codes[f"PARADA {stp}"]
    chk = Mazak_mill.m_codes[f"{chk} BOQUILLA"]
    col = Mazak_mill.m_codes[f"{col} REFRIGERANTE"]

    lines1 = [f"{blk}{stp}{chk}{col}{com}"]
    lines2 = [blank_space]

    return [lines1, lines2]
