from app_tools.format_tools import *


def comment_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar
        side (str): Lado del programa

    Returns:
        list: Lista de líneas de tape
    """

    com, sde, blk = data.values()
    com = " " if com == "" else com

    line = f"(-- {com} --)"

    if sde in ("PRINCIPAL", "LATERAL"):
        lines1 = [line]
        lines2 = [" "]
    elif sde == "SECUNDARIO" and machine in {"K16", "E16"}:
        lines1 = [" "]
        lines2 = [line]
    else:
        lines1 = [" "]
        lines2 = [" "]

    return [lines1, lines2]
