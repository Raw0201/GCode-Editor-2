from PySide6.QtWidgets import QMessageBox


class Messages():

    def data_type_error(self):
        return QMessageBox.critical(
                    self,
                    "Error",
                    "Tipo de datos no válido",
                )

    def blank_data_error(self):
        return QMessageBox.critical(
                    self,
                    "Error",
                    "No puede haber datos en blanco",
                )

    def movement_error(self):
        return QMessageBox.information(
            self,
            "Movimiento no permitido",
            "El encabezado y fin de programa\nno pueden ser movidos",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
            )
