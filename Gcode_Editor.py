# ?
# ? Imports ----------------------------------------------------------------- *
# ?

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import QTranslator, QLibraryInfo, QEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QAbstractItemView,
    QMessageBox,
)

import contextlib
import sys
import os
import json

# ?
# ? Módulos personales ------------------------------------------------------ *
# ?

from app_tools.subwindow_tools import *
from app_tools.format_tools import *
from app_tools.validation_tools import *
from app_tools.message_boxes import *

# ?
# ? Generación de líneas de tape -------------------------------------------- *
# ?

from generators.header_gen import header_gen
from generators.end_gen import end_gen

# ?
# ? Interfaces -------------------------------------------------------------- *
# ?

from interfaces.ui_MainWindow import Ui_MainWindow
from interfaces.ui_helper import Ui_frm_helper
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

        self.subtask1 = None
        self.helper1 = None

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
            "MAZAK",
            "OMNITURN",
            "ROMI",
            "HARDINGE",
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

        self.actionDelete.triggered.connect(self.delete_lines)
        self.actionDuplicate.triggered.connect(self.duplicate_lines)
        self.actionMove_up.triggered.connect(lambda: self.move_lines("up"))
        self.actionMove_down.triggered.connect(lambda: self.move_lines("down"))

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
            self.tape2_widget.hide()

        elif self.current_machine in ("K16", "E16"):
            self.tape2_widget.show()
        elif self.current_machine == "":
            self.tape1_widget.show()
            self.tape2_widget.show()
            self.config_widget.show()

    def load_widgets_events(self) -> None:
        """Cargar eventos de los widgets"""

        self.config_widget.itemClicked.connect(self.config_selected)
        self.config_widget.itemDoubleClicked.connect(self.config_modifier)
        self.tape1_widget.itemSelectionChanged.connect(self.tape1_selected)
        self.tape1_widget.itemDoubleClicked.connect(self.config_modifier)
        self.tape2_widget.itemSelectionChanged.connect(self.tape2_selected)
        self.tape2_widget.itemDoubleClicked.connect(self.config_modifier)

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
        elif machine == "OMNITURN":
            file_name = self.main_tape_number
        elif machine == "ROMI":
            file_name = f"R{self.main_tape_number}"
        elif machine == "HARDINGE":
            file_name = f"H{self.main_tape_number}"
        elif machine == "MAZAK":
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
        self.close()

    def closeEvent(self, event) -> None:
        result = QMessageBox.question(
            self,
            "Cerrar la aplicación",
            "Seguro que desea cerrar?",
            QMessageBox.Yes | QMessageBox.No,
        )
        event.ignore()

        if result == QMessageBox.Yes:
            if self.subtask1:
                self.subtask1.close()
            if self.helper1:
                self.helper1.close()
            event.accept()

    # *
    # * Menú Edición -------------------------------------------------------- *
    # *

    def delete_lines(self) -> None:
        """Borra las líneas seleccionadas"""
        if not self.config_list or not self.current_selection:
            return

        if self.current_selection[0] == 0:
            dialog = QMessageBox.critical(
                self,
                "Borrando encabezado",
                "El encabezado del programa no debe ser borrado",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )
            return

        dialog = QMessageBox.warning(
            self,
            "Borrar líneas",
            "¿Desea borrar las líneas seleccionadas?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )
        if dialog == QMessageBox.Yes:
            start = self.current_selection[0]
            end = self.current_selection[-1] + 1
            del self.config_list[start:end]
            self.update_data()

    def duplicate_lines(self) -> None:
        """Duplica las líneas seleccionadas"""

        index_list = self.current_selection

        if index_list[0] == 0:
            QMessageBox.information(
                self,
                "Duplicando encabezado",
                "El encabezado no puede ser duplicado",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )
            return

        duplicated_lines = [self.config_list[index] for index in index_list]

        insertion_index = index_list[-1] + 1

        for line in duplicated_lines:
            self.config_list.insert(insertion_index, line)
            insertion_index += 1

        selection_len = len(index_list)
        for n, index in enumerate(self.current_selection):
            self.current_selection[n] = index + selection_len

        self.update_data()

    def move_lines(self, direction):

        index_list = self.current_selection
        down_limit = len(self.config_list) - 1

        if self.config_list[index_list[0]][0] in (
            "Inicio de programa",
            # "Fin de programa",
        ):
            Messages.movement_error(self)
            return

        elif index_list[0] == 1 and direction == "up":
            Messages.movement_error(self)
            return

        elif index_list[-1] == down_limit and direction == "down":
            return

        moved_lines = [self.config_list[index] for index in index_list]

        start = index_list[0]
        end = index_list[-1] + 1

        del self.config_list[start:end]

        if direction == "up":
            self.move_up(moved_lines, start)

        else:
            self.move_down(moved_lines, start)

        self.update_data()

    def move_up(self, moved_lines, start):
        index = start - 1
        for line in moved_lines:
            self.config_list.insert(index, line)
            index += 1

        for n, index in enumerate(self.current_selection):
            self.current_selection[n] = index - 1

    def move_down(self, moved_lines, start):
        index = start + 1
        for line in moved_lines:
            self.config_list.insert(index, line)
            index += 1

        for n, index in enumerate(self.current_selection):
            self.current_selection[n] = index + 1

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

        if self.modified_task:
            self.change_modified(data_pack)
        elif not self.current_selection:
            self.insert_end(data_pack)
        else:
            self.insert_after(data_pack)

        self.update_data()

    def insert_after(self, data_pack):
        """Inserta los datos nuevos después de la línea seleccionada

        Args:
            data_pack (list): Datos a insertar
        """

        for pack in data_pack:
            task = pack[0]
            data = pack[1]
            side = pack[2]
            index = self.current_selection[0] + 1
            self.config_list.insert(index, [task, data, side])
            self.current_selection = [index]

    def insert_end(self, data_pack):
        """Inserta los datos nuevos al final de la lista

        Args:
            data_pack (list): Datos a insertar
        """

        for pack in data_pack:
            task = pack[0]
            data = pack[1]
            side = pack[2]
            self.config_list.append([task, data, side])
            self.current_selection = [len(self.config_list) - 1]

    def change_modified(self, data_pack: list) -> None:
        """Modifica los datos de la línea seleccionada

        Args:
            data_pack (list): Lista de datos modificados
        """

        task = data_pack[0][0]
        data = data_pack[0][1]
        side = data_pack[0][2]
        index = self.current_selection[0]
        self.config_list[index] = [task, data, side]

    def update_data(self) -> None:
        """Actualiza pantalla después de abrir"""

        self.activate_all_buttons()
        self.load_tape_conditions()
        self.update_configuration()
        self.tape_add()
        self.update_config_widget()
        self.update_tape_widgets()
        self.config_update_selection()
        self.tape1_update_selection()
        self.tape2_update_selection()

    def tape_add(self) -> None:
        """Genera líneas de tape a partir de la configuración"""

        self.tape1_list = []
        self.tape2_list = []
        self.current_config_line = 0

        for line in self.config_list:
            task = line[0]
            if task != "Inicio de programa":
                self.current_config_line += 1

            self.tasks_list[task].generator(self, line[1], line[2])

    def update_configuration(self) -> None:
        """Actualiza los datos y condiciones del programa"""

        for line in self.config_list:
            task = line[0]
            data = line[1]
            self.tasks_list[task].processor(self, data)
            self.tasks_list[task].button_switcher(self, data)

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

    def tape_generator(self, lines: list, params: list) -> None:
        """Agrega las líneas de tape a las listas

        Args:
            lines (list): Líneas de tape
            param (list): Líneas de parámetros
        """

        par1, par2, par3 = params

        for line in lines[0]:
            if line != "":
                self.tape1_list.append((par1, line, par2, par3))
        for line in lines[1]:
            if line != "":
                self.tape2_list.append((par1, line, par2, par3))

    def config_modifier(self) -> None:
        """Obtiene la línea de configuración a modificar"""

        line = self.current_selection
        task = self.config_list[line[0]][0]
        data = self.config_list[line[0]][1]

        self.tasks_list[task].modifier(self, data)

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

        with contextlib.suppress(AttributeError, IndexError):
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

        with contextlib.suppress(AttributeError, IndexError):
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

        with contextlib.suppress(AttributeError, IndexError):
            for item in all_items:
                item.setSelected(False)
            for item in items:
                item.setSelected(True)
            view = QAbstractItemView
            self.tape2_widget.scrollToItem(items[-1], view.PositionAtCenter)

    # *
    # * Operaciones --------------------------------------------------------- *
    # *

    def helper(self) -> None:
        """Mostrar subventana"""
        if self.helper1:
            del self.helper1
        self.helper1 = Helper()
        self.helper1.show()

    def header(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Header()
        self.subtask1.show()

    def end(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = End()


# ?
# ? Sub clases -------------------------------------------------------------- *
# ?


class Subtask_window(QMainWindow):
    """Clase padre de la ventana de tareas

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica principal
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.setupUi(self)
        self.move(window.subwinpos_horiz, window.subwinpos_verti)
        self.btn_save.clicked.connect(self.collector)
        self.btn_help.clicked.connect(window.helper)

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """

        keyPressed(self, qKeyEvent)

    def closeEvent(self, event) -> None:
        if window.helper1:
            window.helper1.close()


class Helper(QMainWindow, Ui_frm_helper):
    """Ventana de ayuda para la tarea

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica principal
        Ui_frm_helper (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.setupUi(self)

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """

        keyPressed(self, qKeyEvent)


class Header(Subtask_window, Ui_frm_header):
    """Encabezado del programa

    Args:
        Subtask_window (_type_): Clase padre de la ventana
        Ui_frm_header (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)

        self.cbx_mch.addItems(window.machine_list)

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Prt": self.tbx_prt.text(),
            "Pgr": self.tbx_pgr.text(),
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
            Messages.blank_data_error(self)
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
            Messages.data_type_error(self)
            return

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        side = "tape1"
        data1 = (self.task, data, side)
        data_pack = [data1]
        window.config_add(data_pack)
        window.modified_task = False
        self.close()

    def generator(self, data: dict, side: bool) -> None:
        """Genera las líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
            side (bool): Condición de lado del tape
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = header_gen(machine, data, side)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        window.modified_task = True
        prt, pgr, dsc, mch = (data["Prt"], data["Pgr"], data["Dsc"], data["Mch"])

        self.subtask1 = Header()
        self.subtask1.tbx_prt.setText(str(prt))
        self.subtask1.tbx_prt.setSelection(0, 100)
        self.subtask1.tbx_pgr.setText(str(pgr))
        self.subtask1.tbx_dsc.setText(str(dsc))
        self.subtask1.cbx_mch.setCurrentText(str(mch))
        self.subtask1.btn_save.setText("Actualizar")
        self.subtask1.show()

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

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


class End(QMainWindow):
    """Final del programa

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica principal
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)
        self.collector()

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Mch": window.current_machine,
            "Num": window.current_config_line,
        }
        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaquetar los datos a exportar

        Args:
            data (dict): Diccionario de datos recopilados
        """
        side = "tape1"
        data1 = (self.task, data, side)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict, side: bool) -> None:
        """Genera las líneas del tape 1

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data["Mch"] = window.current_machine

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = end_gen(machine, data, side)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        pass

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
        # window.btn_end.setEnabled(False)
        pass


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
