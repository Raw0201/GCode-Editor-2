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


def fversion() -> str:
    """Obtiene la versión del tape según la fecha

    Returns:
        str: Versión del tape
    """

    return date.today().strftime("V%m.%d.%y")
