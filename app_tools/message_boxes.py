from PySide6.QtWidgets import QMessageBox


class Messages:
    def new_tape_question(self):
        return QMessageBox.question(
            self,
            "Nuevo programa",
            "¿Desea comenzar un nuevo programa en blanco?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )

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

    def movement_error_information(self):
        return QMessageBox.information(
            self,
            "Movimiento no permitido",
            "El encabezado y fin de programa\nno deben ser movidos",
        )

    def delete_header_information(self):
        return QMessageBox.information(
            self,
            "Borrando encabezado",
            "El encabezado del programa no debe ser borrado",
        )

    def delete_lines_warning(self):
        return QMessageBox.warning(
            self,
            "Borrar líneas",
            "¿Desea borrar las líneas seleccionadas?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )

    def duplicate_header_information(self):
        return QMessageBox.information(
            self,
            "Duplicando encabezado",
            "El encabezado no debe ser duplicado",
        )
