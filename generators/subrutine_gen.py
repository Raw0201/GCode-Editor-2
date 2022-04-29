from app_tools.format_tools import *


def subrutine_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar
        side (str): Lado del programa

    Returns:
        list: Lista de líneas de tape
    """

    sub, rep, blk = data.values()
    blk = "/" if blk else ""
    rep = f"L{int(rep)}" if rep != "" else ""

    lines1 = [f"{blk}M98P{sub}{rep}"]
    lines2 = [" "]

    return [lines1, lines2]
