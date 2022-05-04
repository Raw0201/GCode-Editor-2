import contextlib
from datetime import date
from app_tools.app_lists import *


def ftext(txt: str) -> str:
    """Formatear texto a mayúsculas

    Args:
        num (str): Texto a formatear

    Returns:
        str: Cadena formateada
    """
    return txt.upper()


def ftape(machine: str, number: int) -> str:
    """Da formato al número de programa

    Args:
        machine (str): Máquina del programa
        number (int): Número de programa

    Returns:
        str: Número de programa formateado
    """

    if machine != "OMNITURN":
        number = str(number)
        if len(number) < 4:
            if machine == "MAZAK":
                while len(number) != 8:
                    number = f"0{number}"
            else:
                while len(number) != 4:
                    number = f"0{number}"

    return number


def foper(oper: str) -> float:
    """Realiza y formatea operaciones matemáticas

    Args:
        oper (str): Operación a evaluar

    Returns:
        float: Resultado de la operación
    """
    if oper != "":
        try:
            result = eval(oper)
            result = float(fnum4(result))
        except NameError:
            result = 0
    return result


def fdia(num: str) -> str:
    """Formatear dimensiones a 3 decimales

    Args:
        num (str): Número a formatear

    Returns:
        str: Cadena formateada
    """

    num = "{0:.3f}".format(float(num))

    while True:
        if num[0] == "-":
            if num[1] != "0":
                break
            num = f"-{num[2:]}"
        elif num[0] != "0":
            break
        else:
            num = num[1:]
    num = "0" if num == ".0" else num

    return num


def fnum3(num: str) -> str:
    """Formatear de float a str 3 decimales

    Args:
        num (str): Número a formatear

    Returns:
        str: Cadena formateada
    """
    num = "{0:.3f}".format(float(num))

    while num[-1] == "0" and num[-2] != ".":
        num = num[:-1]

    while True:
        if num[0] == "-":
            if num[1] != "0":
                break
            num = f"-{num[2:]}"
        elif num[0] != "0":
            break
        else:
            num = num[1:]
    num = "0" if num == ".0" else num

    return num


def fnum4(num: str) -> str:
    """Formatear de float a str 4 decimales

    Args:
        num (str): Número a formatear

    Returns:
        str: Cadena formateada
    """
    num = "{0:.4f}".format(float(num))

    while num[-1] == "0" and num[-2] != ".":
        num = num[:-1]

    while True:
        if num[0] == "-":
            if num[1] != "0":
                break
            num = f"-{num[2:]}"
        elif num[0] != "0":
            break
        else:
            num = num[1:]
    num = "0" if num == ".0" else num

    return num


def fversion() -> str:
    """Obtiene la versión del tape según la fecha

    Returns:
        str: Versión del tape
    """

    return date.today().strftime("V%m.%d.%y")


def fspace() -> str:
    """Devuelve un espacio vacío para visualización

    Returns:
        str: Espacio vacío
    """
    return "  "


def kswiss_to_swiss(tool: int, side: str) -> int:
    """Convierte números de herramienta desde K

    Args:
        tool (int): Número de herramienta
        side (str): Husillo utilizado

    Returns:
        int: Número de herramienta convertido
    """

    tools1 = {1: 11, 2: 12, 3: 13, 4: 14, 5: 15}
    tools2 = {11: 16, 12: 17, 13: 18, 14: 18}

    if side == "PRINCIPAL" and tool in tools1:
        tool = tools1[tool]
    elif side == "LATERAL" and tool in tools2:
        tool = tools2[tool]

    return tool


def swiss_to_kswiss(tool: int, side: str) -> int:
    """Convierte números de herramienta hacia K

    Args:
        tool (int): Número de herramienta
        side (str): Husillo utilizado

    Returns:
        int: Número de herramienta convertido
    """

    tools1 = {11: 1, 12: 2, 13: 3, 14: 4, 15: 5}
    tools2 = {16: 11, 17: 12, 18: 13}

    if side == "PRINCIPAL" and tool in tools1:
        tool = tools1[tool]
    elif side == "LATERAL" and tool in tools2:
        tool = tools2[tool]

    return tool


def fcom(tool: int, compensations: list) -> float:
    return compensations[tool] if tool in compensations else False
