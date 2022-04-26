# ?
# ? Imports ----------------------------------------------------------------- *
# ?

from PySide6 import QtCore
from PySide6.QtCore import QTranslator, QLibraryInfo, QEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QTableWidgetSelectionRange,
    QFileDialog,
    QAbstractItemView,
    QMessageBox,
    QMenu,
)

import contextlib
import sys
import os
import json
import math

# ?
# ? Módulos personales ------------------------------------------------------ *
# ?

from subwindow_tools import *
from format_tools import *
from validation_tools import *

# ?
# ? Interfaces -------------------------------------------------------------- *
# ?

from interfaces.ui_MainWindow import Ui_MainWindow
from interfaces.ui_header import Ui_frm_header

# ?
# ? Clase principal --------------------------------------------------------- *
# ?


class MainWindow(QMainWindow, Ui_MainWindow):
    """Ventana principal del programa

    Args:
        QMainWindow (_type_): Clase de interfaz gráfica
        Ui_MainWindow (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializa la ventana"""

        super().__init__()
        self.setupUi(self)

        self.load_machine_list()
        self.load_folders_locations()
        self.load_default_folders()
        self.load_main_data()
        self.load_machining_data()
        self.load_tape_conditions()
        self.load_task_list()
        self.load_menu_actions()
        self.load_buttons_list()
        self.load_buttons_connections()
        self.load_buttons_status()
        self.load_widgets()
        self.load_widgets_events()
        self.load_main_title()

    # *
    # * Carga inicial de datos ---------------------------------------------- *
    # *

    def load_machine_list(self) -> None:
        """Cargar lista de máquinas"""
        self.machine_list = (
            "B12",
            "A16",
            "K16",
            "E16",
            "Mazak",
            "OmniTurn",
            "Romi",
            "Hardinge",
        )

    def load_folders_locations(self) -> None:
        """Ubicación de los folders de guardado"""

        self.root_dir = "C:/GCodeEditor"

        base = self.root_dir
        self.default_dirs = {
            machine: f"{base}/{machine}" for machine in self.machine_list
        }

    def load_default_folders(self) -> None:
        """Crear folders para guardar los tapes"""

        with contextlib.suppress(FileExistsError):
            os.mkdir(self.root_dir)
        for folder in self.default_dirs:
            default_folder = f"{self.root_dir}/{folder}"
            with contextlib.suppress(FileExistsError):
                os.mkdir(default_folder)
        os.chdir(self.root_dir)

    def load_main_data(self) -> None:
        """Cargar datos principales"""

        self.current_folder = self.root_dir
        self.current_machine = ""
        self.file_name = ""
        self.file_extension = ""
        self.part_name = ""
        self.main_tape_number = ""
        self.sub_tape_number = ""
        self.tape_description = ""
        self.subwinpos_horiz = 0
        self.subwinpos_verti = 0
        self.current_config_line = 0
        self.config_list = []
        self.current_selection = []
        self.tape1_list = []
        self.tape2_list = []

    def load_machining_data(self) -> None:
        """Cargar datos de mecanizado"""

        self.current_comment = ""
        self.current_work_shift = ""
        self.material_lenght = 0
        self.material_widht = 0
        self.current_tool = 0
        self.current_tool_dia = 0
        self.main_program_data = []
        self.lineal_matrix_horiz = []
        self.lineal_matrix_verti = []
        self.square_matrix_horiz = []
        self.square_matrix_verti = []
        self.plate_matrix_horiz = []
        self.plate_matrix_verti = []
        self.swiss_back_machining = False

    def load_tape_conditions(self) -> None:
        """Cargar condiciones del tape"""

        self.modified_task = False
        self.save_required = False
        self.tool_close_required = False
        self.milling_close_required = False
        self.drilling_close_required = False
        self.start_of_tape_required = True
        self.end_of_tape_required = True

    def load_task_list(self) -> None:
        """Cargar lista de tareas"""

        self.tasks_list = {
            "Inicio de programa": Header,
            "Fin de programa": End,
        }

    def load_menu_actions(self) -> None:
        """Cargar acciones del menú"""

        self.actionNew.triggered.connect(self.new_tape)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_config)
        self.actionClose.triggered.connect(self.close_app)

    def load_buttons_list(self) -> None:
        """Cargar lista de botones"""

        self.main_buttons = {
            self.btn_header: self.header,
            self.btn_end: self.end,
        }

        self.turning_buttons = {}

        self.milling_buttons = {}

        self.drilling_buttons = {}

        self.plate_buttons = {}

    def load_buttons_connections(self) -> None:
        """Cargar conexiones de botones a funciones"""

        for button in self.main_buttons.keys():
            button.clicked.connect(self.main_buttons[button])

    def load_buttons_status(self) -> None:
        """Actualiza estado de los botones"""

        for button_list in (
            self.main_buttons,
            self.turning_buttons,
            self.milling_buttons,
            self.drilling_buttons,
            self.plate_buttons,
        ):
            for button in button_list:
                button.setEnabled(False)

        self.btn_header.setEnabled(True)

    def activate_all_buttons(self) -> None:
        """Activa todos los botones"""

        for button_list in (
            self.main_buttons,
            self.turning_buttons,
            self.milling_buttons,
            self.drilling_buttons,
            self.plate_buttons,
        ):
            for button in button_list:
                button.setEnabled(True)

    def load_widgets(self) -> None:
        """Ocultar ventanas de tape y configuración"""

        # self.config_widget.hide()
        if self.current_machine in (
            "B12",
            "A16",
            "Mazak",
            "OmniTurn",
            "Romi",
            "Hardinge",
        ):
            # self.tape2_widget.hide()
            pass

        elif self.current_machine in ("K16", "E16"):
            self.tape2_widget.show()
        elif self.current_machine == "":
            self.tape1_widget.show()
            self.tape2_widget.show()
            self.config_widget.show()

    def load_widgets_events(self) -> None:
        """Cargar eventos de los widgets"""

        self.config_widget.itemClicked.connect(self.config_selected)
        # self.config_widget.itemDoubleClicked.connect(self.config_modify)
        self.tape1_widget.itemSelectionChanged.connect(self.tape1_selected)
        # self.tape1_widget.itemDoubleClicked.connect(self.tape_modify)
        self.tape2_widget.itemSelectionChanged.connect(self.tape2_selected)
        # self.tape2_widget.itemDoubleClicked.connect(self.tape_modify_2)

    def load_main_title(self) -> None:
        """Actualiza el título de la ventana"""

        app_name = "G-Code Editor"
        machine_type = self.current_machine
        file_name = self.file_name
        file_extension = self.file_extension
        folder = self.current_folder
        file = f"{file_name}{file_extension}"
        tape_name = f"- {folder}/{file} - " if file_name != "" else ""
        tape_description = f"{self.tape_description}"
        save_status = "*" if self.save_required else ""

        app_machine = f"{app_name} {machine_type}"
        tape_data = f"{tape_name} {tape_description}"
        main_title = f"{app_machine}  {tape_data} {save_status}"

        self.setWindowTitle(main_title)

    def update_file_name(self) -> None:
        """Actualiza el nombre del archivo"""

        back = "(H)" if self.swiss_back_machining else ""
        machine = self.current_machine
        file_extension = ""

        if machine in ("B12", "A16", "K16", "E16"):
            file_name = f"({self.current_machine}) {self.part_name} {back}"
            file_extension = ".CNC"
        elif machine == "OmniTurn":
            file_name = self.main_tape_number
        elif machine == "Romi":
            file_name = f"R{self.main_tape_number}"
        elif machine == "Hardinge":
            file_name = f"H{self.main_tape_number}"
        elif machine == "Mazak":
            file_name = f"O{self.main_tape_number}"
            file_extension = ".CNC"

        self.file_name = file_name
        self.file_extension = file_extension

    def update_file_dir(self) -> None:
        """Actualiza el forder de guardado"""

        self.current_folder = self.default_dirs[self.current_machine]
        os.chdir(self.current_folder)

    # *
    # * Menú Archivo -------------------------------------------------------- *
    # *

    def new_tape(self) -> None:
        """Crear un nuevo tape"""

        dialog = QMessageBox.warning(
            self,
            "Nuevo programa",
            "¿Desea comenzar un nuevo programa en blanco?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )
        if dialog == QMessageBox.Yes:
            self.load_main_data()
            self.load_machining_data()
            self.load_tape_conditions()
            self.load_buttons_status()
            self.load_widgets()
            self.load_main_title()

            self.config_widget.clearContents()
            self.tape1_widget.clearContents()
            self.tape2_widget.clearContents()
            self.config_widget.setRowCount(0)
            self.tape1_widget.setRowCount(0)
            self.tape2_widget.setRowCount(0)

    def open_file(self) -> None:
        """Abrir un archivo de configuración"""
        try:
            os.chdir(self.current_folder)
            file_name = QFileDialog.getOpenFileName(
                self,
                caption=("Abrir programa"),
                dir=self.current_folder,
                filter=("Archivos de configuración (*.json)"),
            )

            with open(file_name[0]) as file:
                self.config_list = json.load(file)

            self.current_folder = os.path.dirname(file_name[0])
            os.chdir(self.current_folder)

            self.update_data()
            self.save_required = False
            self.load_main_title()

        except OSError:
            return

    def save_config(self) -> None:
        """Guardar el archivo de configuración"""

        if not self.tape1_list:
            return

        self.update_file_dir()
        file = f"{self.file_name}.json"
        with open(file, "w") as file:
            json.dump(self.config_list, file)
        self.save_tape()

    def save_tape(self) -> None:
        """Guardar el archivo de configuración"""

        if not self.tape1_list:
            return

        os.chdir(self.root_dir)
        tape_complete = self.tape1_list + self.tape2_list

        file = f"{self.file_name}{self.file_extension}"
        with open(file, "w") as tape:
            for lines in tape_complete:
                tape.write(lines[1] + "\n")

        self.save_required = False
        self.load_main_title()

    def close_app(self) -> None:
        """Cerrar la aplicación"""

        dialog = QMessageBox.warning(
            self,
            "Cerrar la aplicación",
            "¿Desea cerrar la aplicación?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )
        if dialog == QMessageBox.Yes:
            self.close()

    # *
    # * Menú Edición -------------------------------------------------------- *
    # *

    # *
    # * Menú Ayuda ---------------------------------------------------------- *
    # *

    # *
    # * Ingreso de datos ---------------------------------------------------- *
    # *

    def config_add(self, data_pack: list) -> None:
        """Actualizar archivo de configuración y tape según datos ingresados

        Args:
            task (str): Nombre de la tarea
            data (list): Paquete de datos de la tarea
        """
        for pack in data_pack:
            task = pack[0]
            data = pack[1]
            self.config_list.append([task, data])
        self.update_data()

    def update_data(self) -> None:
        """Actualiza pantalla después de abrir"""
        self.current_machine = self.config_list[0][1][0]["Mch"]

        self.activate_all_buttons()
        self.load_tape_conditions()
        self.tape_add()
        self.update_configuration()
        self.update_config_widget()
        self.update_tape_widgets()

    def tape_add(self) -> None:
        """Genera líneas de tape a partir de la configuración"""

        self.tape1_list = []
        self.tape2_list = []
        self.current_config_line = 0

        for line in self.config_list:
            task = line[0]
            if task != "Inicio programa":
                self.current_config_line += 1

            self.tasks_list[task].generator1(self, line[1][0])
            self.tasks_list[task].generator2(self, line[1][1])

    def update_configuration(self) -> None:
        """Actualiza los datos y condiciones del programa"""

        for line in self.config_list:
            task = line[0]
            self.tasks_list[task].processor(self, line[1][0])
            self.tasks_list[task].button_switcher(self, line[1][0])

    def get_parameters(self) -> list:
        """Obtiene los parámetros de configuración para tape

        Returns:
            list: Lista de parámetros
        """
        return (
            self.current_config_line,
            self.current_tool,
            self.current_comment,
        )

    # *
    # * Funciones de widgets ------------------------------------------------ *
    # *

    def update_config_widget(self) -> None:
        """Actualiza ventana de configuración"""

        config = self.config_list
        self.config_widget.setRowCount(len(config))
        for num, line in enumerate(config):
            operation = line[0]
            self.config_widget.setItem(num, 0, QTableWidgetItem(operation))

    def update_tape_widgets(self) -> None:
        """Actualiza ventanas de tape"""

        self.tape1_widget.setRowCount(len(self.tape1_list))
        for num, line in enumerate(self.tape1_list):
            self.tape1_widget.setItem(num, 0, QTableWidgetItem(line[1]))

        self.tape2_widget.setRowCount(len(self.tape2_list))
        for num, line in enumerate(self.tape2_list):
            self.tape2_widget.setItem(num, 0, QTableWidgetItem(line[1]))

    def config_selected(self) -> None:
        """Devuelve las líneas seleccionadas de la configuración"""
        if selected_items := self.config_widget.selectedItems():
            config_lines = []
            config_lines.extend(
                item.row() for item in selected_items if item.column() == 0
            )
            self.current_selection = sorted(list(set(config_lines)))
            self.tape1_update_selection()
            self.tape2_update_selection()

    def tape1_selected(self) -> None:
        """Devuelve las líneas seleccionadas de la configuración"""
        if selected_items := self.tape1_widget.selectedItems():
            selected_list = []
            selected_list.extend(
                item.row() for item in selected_items if item.column() == 0
            )
            config_lines = [self.tape1_list[line][0] for line in selected_list]
            self.current_selection = sorted(list(set(config_lines)))
            self.config_update_selection()
            self.tape2_update_selection()

    def tape2_selected(self) -> None:
        """Devuelve las líneas seleccionadas de la configuración"""
        if selected_items := self.tape2_widget.selectedItems():
            selected_list = []
            selected_list.extend(
                item.row() for item in selected_items if item.column() == 0
            )
            config_lines = [self.tape1_list[line][0] for line in selected_list]
            self.current_selection = sorted(list(set(config_lines)))
            self.config_update_selection()

    def config_update_selection(self) -> None:
        """Actualiza líneas seleccionadas en config"""

        all_items = [
            self.config_widget.item(index_number, 0)
            for index_number in range(len(self.config_list))
        ]

        indexes = self.current_selection
        items = [self.config_widget.item(index, 0) for index in indexes]

        with contextlib.suppress(AttributeError):
            for item in all_items:
                item.setSelected(False)
            for item in items:
                item.setSelected(True)
            view = QAbstractItemView
            self.config_widget.scrollToItem(items[-1], view.PositionAtCenter)

    def tape1_update_selection(self) -> None:
        """Actualiza líneas seleccionadas en tape1"""

        all_items = [
            self.tape1_widget.item(index_number, 0)
            for index_number in range(len(self.tape1_list))
        ]

        config_indexes = self.current_selection
        indexes = [
            num
            for num, index in enumerate(self.tape1_list)
            if index[0] in config_indexes
        ]
        items = [self.tape1_widget.item(index, 0) for index in indexes]

        with contextlib.suppress(AttributeError):
            for item in all_items:
                item.setSelected(False)
            for item in items:
                item.setSelected(True)
            view = QAbstractItemView
            self.tape1_widget.scrollToItem(items[-1], view.PositionAtCenter)

    def tape2_update_selection(self) -> None:
        """Actualiza líneas seleccionadas en tape1"""

        all_items = [
            self.tape2_widget.item(index_number, 0)
            for index_number in range(len(self.tape2_list))
        ]

        config_indexes = self.current_selection
        indexes = [
            num
            for num, index in enumerate(self.tape2_list)
            if index[0] in config_indexes
        ]
        items = [self.tape2_widget.item(index, 0) for index in indexes]

        with contextlib.suppress(AttributeError):
            for item in all_items:
                item.setSelected(False)
            for item in items:
                item.setSelected(True)
            view = QAbstractItemView
            self.tape2_widget.scrollToItem(items[-1], view.PositionAtCenter)

    # *
    # * Operaciones --------------------------------------------------------- *
    # *

    def header(self) -> None:
        """Mostrar subventana"""
        self.header1 = Header()
        self.header1.show()

    def end(self) -> None:
        """Mostrar subventana"""
        self.end1 = End()


# ?
# ? Sub clases -------------------------------------------------------------- *
# ?


class Header(QMainWindow, Ui_frm_header):
    """Encabezado del programa

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica
        Ui_frm_header (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la ventana"""

        super().__init__()
        self.setupUi(self)
        self.move(window.subwinpos_horiz, window.subwinpos_verti)
        self.task = find_task_name(window.tasks_list, __class__)
        self.cbx_mch.addItems(window.machine_list)
        self.btn_save.clicked.connect(self.collector)

        self.cbx_mch.setCurrentText(
            window.current_machine
        ) if window.current_machine != "" else ""

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Prt": self.tbx_prt.text(),
            "Pgr": self.tbx_prg.text(),
            "Dsc": self.tbx_dsc.text(),
            "Mch": self.cbx_mch.currentText(),
        }
        self.validator(data)

    def validator(self, data: dict) -> None:
        """Validar datos ingresados por el usuario

        Args:
            data (dict): Diccionario de datos recopilados
        """

        if any_empty(data):
            QMessageBox.critical(
                self,
                "Error",
                "No puede haber datos en blanco",
            )
            return
        self.converter(data)

    def converter(self, data: dict) -> None:
        """Convertir los datos al formato requerido

        Args:
            data (dict): Diccionario de datos recopilados
        """

        try:
            data["Prt"] = ftext(data["Prt"]) if data["Prt"] != "" else ""
            data["Pgr"] = ftext(data["Pgr"]) if data["Pgr"] != "" else ""
            data["Dsc"] = ftext(data["Dsc"]) if data["Dsc"] != "" else ""
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "Tipo de datos no válido",
            )
            return
        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaquetar los datos a exportar

        Args:
            data (dict): Diccionario de datos recopilados
        """
        data_1 = (
            "Fin de programa",
            ({"Dta": "Fin de programa1"}, {"Dta": "Fin de programa2"}),
        )
        data_2 = (
            "Fin de programa",
            ({"Dta": "Fin de programa3"}, {"Dta": "Fin de programa4"}),
        )

        data_pack = [(self.task, (data, {})), data_1, data_2]
        window.config_add(data_pack)
        self.close()

    def generator1(self, data: dict) -> None:
        """Genera las líneas del tape 1

        Args:
            data (dict): Diccionario de datos recopilados
        """
        par = window.get_parameters()
        lines = ["Línea tape 1"]

        for line in lines:
            if line != "":
                window.tape1_list.append((par[0], line, par[1], par[2]))

    def generator2(self, data: dict) -> None:
        """Genera las líneas del tape 2

        Args:
            data (dict): Diccionario de datos recopilados
        """
        par = window.get_parameters()
        lines = ["Línea tape 2"]

        for line in lines:
            if line != "":
                window.tape2_list.append((par[0], line, par[1], par[2]))

    def processor(self, data: dict) -> None:
        """Procesar los datos ingresados por el usuario

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.start_of_tape_required = False
        window.modified_task = False
        window.save_required = True

        window.current_machine = data["Mch"]
        window.part_name = data["Prt"]
        window.main_tape_number = data["Pgr"]
        window.tape_description = data["Dsc"]

        window.update_file_name()
        window.update_file_dir()
        window.load_main_title()
        window.load_widgets()

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        for button_list in (
            window.main_buttons,
            window.turning_buttons,
            window.milling_buttons,
            window.drilling_buttons,
        ):
            for button in button_list:
                button.setEnabled(True)

        if data["Mch"] != "Mazak":
            for button in window.plate_buttons:
                button.setEnabled(False)

        if data["Mch"] == "Mazak":
            for button in window.turning_buttons:
                button.setEnabled(False)

        window.btn_header.setEnabled(False)

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """

        keyPressed(self, qKeyEvent)


class End(QMainWindow):
    """Final del programa

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica
    """

    def __init__(self) -> None:
        """Inicializar la ventana"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)
        data = {"Dta": "Fin de programa"}
        self.converter(data)

    # def collector(self) -> None:
    #     """Recopilar datos ingresado por el usuario"""

    #     data = {
    #         "Prt": self.tbx_prt.text(),
    #         "Pgr": self.tbx_prg.text(),
    #         "Dsc": self.tbx_dsc.text(),
    #         "Mch": self.cbx_mch.currentText(),
    #     }
    #     self.validator(data)

    # def validator(self, data: dict) -> None:
    #     """Validar datos ingresados por el usuario

    #     Args:
    #         data (dict): Diccionario de datos recopilados
    #     """

    #     if any_empty(data):
    #         QMessageBox.critical(
    #             self,
    #             "Error",
    #             "No puede haber datos en blanco",
    #         )
    #         return
    #     self.converter(data)

    def converter(self, data: dict) -> None:
        """Convertir los datos al formato requerido

        Args:
            data (dict): Diccionario de datos recopilados
        """
        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaquetar los datos a exportar

        Args:
            data (dict): Diccionario de datos recopilados
        """
        data_pack = [(self.task, (data, data))]
        window.config_add(data_pack)
        self.close()

    def generator1(self, data: dict) -> None:
        """Genera las líneas del tape 1

        Args:
            data (dict): Diccionario de datos recopilados
        """
        par = window.get_parameters()
        lines = [data["Dta"]]

        for line in lines:
            if line != "":
                window.tape1_list.append((par[0], line, par[1], par[2]))

    def generator2(self, data: dict) -> None:
        """Genera las líneas del tape 2

        Args:
            data (dict): Diccionario de datos recopilados
        """
        par = window.get_parameters()
        lines = [data["Dta"]]

        for line in lines:
            if line != "":
                window.tape2_list.append((par[0], line, par[1], par[2]))

    def processor(self, data: dict) -> None:
        """Procesar los datos ingresados por el usuario

        Args:
            data (dict): Diccionario de datos recopilados
        """
        window.save_required = True

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """
        pass

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """

        keyPressed(self, qKeyEvent)


# ?
# ? Creación de ventana principal ------------------------------------------- *
# ?


if __name__ == "__main__":
    app = QApplication(sys.argv)

    translator = QTranslator(app)
    translations = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load("qt_es", translations)
    app.installTranslator(translator)

    window = MainWindow()
    window.show()
    window.setWindowState(QtCore.Qt.WindowMaximized)
    sys.exit(app.exec())
