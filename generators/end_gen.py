from app_tools.format_tools import *


def end_gen(machine: str, data: list) -> list:
    """Generador

    Args:
        machine (str): Tipo de máquina utilizada
        data (list): Lista de datos a procesar

    Returns:
        list: Lista de líneas de tape
    """

    mch, num, blk = data.values()

    lines1 = [f"Finalizando tape1 de {mch} {num}"]
    lines2 = [f"Finalizando tape2 de {mch} {num}"]

    return [lines1, lines2]
