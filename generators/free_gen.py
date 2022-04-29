from app_tools.format_tools import *


def free_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar
        side (str): Lado del programa

    Returns:
        list: Lista de líneas de tape
    """

    fre, sde, blk = data.values()
    blk = "/" if blk else ""
    blk = "" if fre == "" else blk
    fre = " " if fre == "" else fre

    line = f"{blk}{fre}"

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
