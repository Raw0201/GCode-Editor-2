def all_empty(data: dict) -> bool:
    """Verificar si todos los campos están vacíos

    Args:
        data (dict): Diccionario de datos recopilados

    Returns:
        bool: Condición de los campos
    """
    items_list = list(data.items())
    filtered_list = items_list[1:]
    empties = sum(item[1] == "" for item in filtered_list)
    if empties == len(data) - 1:
        return True


def any_empty(data: dict) -> bool:
    """Verificar si algún campo está vacío

    Args:
        data (dict): Diccionario de datos recopilados

    Returns:
        bool: Condición de los campos
    """
    empties = sum(value == "" for _, value in data.items())
    if empties > 0:
        return True
