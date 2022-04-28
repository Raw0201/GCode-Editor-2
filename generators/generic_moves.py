class Data():
    """Datos genéricos"""

    def generic_end(self, number: int) -> list:
        """Fin de programa genérico para pruebas

        Args:
            number (int): Número a colocar

        Returns:
            list: Lista de parámetros
        """

        return (
            "Fin de programa",
            (
                {"Dta": f"Fin de programa{number}"},
                {"Dta": f"Fin de programa{number + 1}"},
            ),
        )


class Movement():
    """Movimientos genéricos"""

    def z_exit(self, distance: float) -> list:
        """Movimiento de salida en Z

        Args:
            distance (float): Distancia de salida

        Returns:
            list: Lista de parámetros
        """

        return f"Salida de Z{distance}"
