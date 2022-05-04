from app_tools.format_tools import *


def comment_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    com, sde, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""
    com = " " if com == "" else com
    line = f"{blk}(-- {com} --)"

    if sde != "SECUNDARIO":
        lines1 = [line]
        lines2 = [blank_space]
    elif machine in {"K16", "E16"}:
        lines1 = [blank_space]
        lines2 = [line]
    else:
        lines1 = [blank_space]
        lines2 = [blank_space]

    return [lines1, lines2]
