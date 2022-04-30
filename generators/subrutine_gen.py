from app_tools.format_tools import *


def subrutine_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    sub, rep, blk = data.values()
    blank_space = fspace()

    blk = "/" if blk else ""
    rep = f"L{int(rep)}" if rep != "" else ""

    lines1 = [f"{blk}M98P{sub}{rep}"]
    lines2 = [blank_space]
    return [lines1, lines2]
