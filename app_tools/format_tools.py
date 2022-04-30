from datetime import date


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
    if machine != "OmniTurn":
        number = str(number)
        if len(number) < 4:
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
