# ?
# ? Imports ----------------------------------------------------------------- *
# ?

from PySide6 import QtCore
from PySide6.QtCore import QTranslator, QLibraryInfo
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QAbstractItemView,
    QMessageBox,
)

import pyqtgraph as pg
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
from app_tools.app_lists import *


# ?
# ? Generación de líneas de tape -------------------------------------------- *
# ?

from generators.header_gen import header_gen
from generators.free_gen import free_gen
from generators.comment_gen import comment_gen
from generators.subrutine_gen import subrutine_gen
from generators.tool_call_gen import tool_call_gen
from generators.tool_close_gen import tool_close_gen
from generators.spindle_gen import spindle_gen
from generators.end_gen import end_gen

# ?
# ? Interfaces -------------------------------------------------------------- *
# ?

from interfaces.ui_MainWindow import Ui_MainWindow
from interfaces.ui_graph import Ui_GraphWindow
from interfaces.ui_helper import Ui_frm_helper
from interfaces.ui_header import Ui_frm_header
from interfaces.ui_comment import Ui_frm_comment
from interfaces.ui_subrutine import Ui_frm_subrutine
from interfaces.ui_tool_call import Ui_frm_tool_call
from interfaces.ui_spindle import Ui_frm_spindle
from interfaces.ui_version import Ui_frm_version

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
        self.graph1 = None

        self.load_folders_locations()
        self.load_default_folders()
        self.load_main_data()
        self.load_machining_data()
        self.load_tape_conditions()
        self.load_task_list()
        self.load_menu_actions()
        self.load_buttons_list()
        self.load_buttons_connections()
        self.default_buttons_status()
        self.load_widgets_events()
        self.load_main_title()

    # *
    # * Carga inicial de datos ---------------------------------------------- *
    # *

    def load_folders_locations(self) -> None:
        """Ubicación de los folders de guardado"""

        self.root_dir = "C:/GCodeEditor"

        base = self.root_dir
        self.default_dirs = {
            machine: f"{base}/{machine}" for machine in Lists.machine_list
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

        self.current_widget = ""
        self.current_folder = self.root_dir
        self.file_name = ""
        self.file_extension = ""
        self.subwinpos_horiz = 0
        self.subwinpos_verti = 0
        self.current_config_line = 0
        self.config_list = []
        self.current_selection = []
        self.tape1_list = []
        self.tape2_list = []

    def load_machining_data(self) -> None:
        """Cargar datos de mecanizado"""

        self.current_machine = ""
        self.current_comment = ""
        self.current_side = ""
        self.current_work_offset = ""
        self.part_name = ""
        self.main_tape_number = ""
        self.tape_description = ""
        self.current_bar_diameter = 0
        self.current_part_lenght = 0
        self.current_tool = 0
        self.current_tool_diameter = 0
        self.swiss_back_machining = False

    def load_tape_conditions(self) -> None:
        """Cargar condiciones del tape"""

        self.modified_task = False
        self.save_required = False

    def load_task_list(self) -> None:
        """Cargar lista de tareas"""

        self.tasks_list = {
            "Inicio de programa": Header,
            "        Comentario": Comment,
            " ": Free,
            "        -> Subrutina": Subrutine,
            "    Llamar herramienta": Tool_call,
            "    Cerrar herramienta": Tool_close,
            "        Giro husillo": Spindle,
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
        self.actionBlock.triggered.connect(self.block_lines)
        self.actionMove_up.triggered.connect(lambda: self.movement("up"))
        self.actionMove_down.triggered.connect(lambda: self.movement("down"))
        self.actionGraph.triggered.connect(self.graph)
        self.actionVersion.triggered.connect(self.version)

    def load_buttons_list(self) -> None:
        """Cargar lista de botones"""

        self.main_buttons = {
            self.btn_header: self.header,
            self.btn_end: self.end,
            self.btn_free: self.free,
            self.btn_comment: self.comment,
            self.btn_subrutine: self.subrutine,
            self.btn_tool_call: self.tool_call,
            self.btn_tool_close: self.tool_close,
            self.btn_spindle: self.spindle,
        }

        self.turning_buttons = {}

        self.milling_buttons = {}

        self.drilling_buttons = {}

        self.plate_buttons = {}

    def load_buttons_connections(self) -> None:
        """Cargar conexiones de botones a funciones"""

        for button in self.main_buttons.keys():
            button.clicked.connect(self.main_buttons[button])

    def default_buttons_status(self) -> None:
        """Actualiza estado inicial de los botones"""

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

    def load_widgets_events(self) -> None:
        """Cargar eventos de los widgets"""

        self.config_widget.clicked.connect(self.config_clicked)
        self.tape1_widget.clicked.connect(self.tape1_clicked)
        self.tape2_widget.clicked.connect(self.tape2_clicked)
        self.config_widget.itemSelectionChanged.connect(self.config_selected)
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

        dialog = Messages.new_tape_question(self)
        if dialog == QMessageBox.Yes:
            self.create_new_tape()

    def create_new_tape(self):
        """Crea el nuevo tape"""

        self.load_main_data()
        self.load_machining_data()
        self.load_tape_conditions()
        self.default_buttons_status()
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
        except KeyError:
            Messages.file_open_error(self)
            self.create_new_tape()

    def save_config(self) -> None:
        """Guardar el archivo de configuración"""

        if not self.tape1_list:
            return

        self.update_data()
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
        complete_tape = self.make_tape()

        file = f"{self.file_name}{self.file_extension}"
        with open(file, "w") as tape:
            for lines in complete_tape:
                tape.write(lines + "\n")

        self.save_required = False
        self.load_main_title()

    def make_tape(self) -> list:
        """Crea las líneas del tape

        Returns:
            list: Tape completo
        """

        tape = []
        blank_space = fspace()

        for line in self.tape1_list:
            data = line[1]
            if data != blank_space:
                tape.append(data)
        for line in self.tape2_list:
            data = line[1]
            if data != blank_space:
                tape.append(data)

        return tape

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
            dialog = Messages.delete_header_information(self)
            return

        dialog = Messages.delete_lines_warning(self)

        if dialog == QMessageBox.Yes:
            start = self.current_selection[0]
            end = self.current_selection[-1] + 1
            del self.config_list[start:end]
            self.update_data()

    def duplicate_lines(self) -> None:
        """Duplica las líneas seleccionadas"""

        index_list = self.current_selection
        if index_list[0] == 0:
            Messages.duplicate_header_information(self)
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

    def movement(self, direction: str) -> None:
        """Valida el movimiento de las líneas seleccionadas

        Args:
            direction (str): Dirección del movimiento
        """

        index_list = self.current_selection

        down_limit = len(self.config_list) - 1
        if self.config_list[index_list[0]][0] in (
            "Inicio de programa",
            # "Fin de programa",
        ):
            Messages.movement_error_information(self)
            return
        elif index_list[0] == 1 and direction == "up":
            Messages.movement_error_information(self)
            return
        elif index_list[-1] == down_limit and direction == "down":
            return

        self.move_lines(index_list, direction)

    def move_lines(self, index_list: list, direction: str) -> None:
        """Mueve las líneas de configuración

        Args:
            index_list (list): Lista de índices a mover
            direction (str): Dirección del movimiento
        """

        moved_data = [self.config_list[index] for index in index_list]
        start, end = index_list[0], index_list[-1] + 1
        del self.config_list[start:end]

        increment = 1 if direction == "down" else -1
        index = start + increment
        for line in moved_data:
            self.config_list.insert(index, line)
            index += 1

        for n, index in enumerate(self.current_selection):
            self.current_selection[n] = index + increment

        self.update_data()

    def home_position(self) -> None:
        """Obtiene la línea inicial del programa"""
        line = 0
        self.go_to_position(line)

    def end_position(self) -> None:
        """Obtiene la línea final del programa"""
        line = len(self.config_list) - 1
        self.go_to_position(line)

    def go_to_position(self, line):
        """Ir a la línea indicada"""
        self.config_widget.setCurrentCell(line, 0)
        self.current_selection = [line]
        self.tape1_update_selection()
        self.tape2_update_selection()

    # *
    # * Menú Modificar ------------------------------------------------------ *
    # *

    def block_lines(self) -> None:
        """Bloquea o desbloquea las líneas seleccionadas"""

        index_list = self.current_selection
        for index in index_list:
            with contextlib.suppress(KeyError):
                block = self.config_list[index][1]["Blk"]
                self.config_list[index][1]["Blk"] = not block
        self.update_data()

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

    def insert_after(self, data_pack: list):
        """Inserta los datos nuevos después de la línea seleccionada

        Args:
            data_pack (list): Datos a insertar
        """

        for pack in data_pack:
            task = pack[0]
            data = pack[1]
            index = self.current_selection[0] + 1
            self.config_list.insert(index, [task, data])
            self.current_selection = [index]

    def insert_end(self, data_pack):
        """Inserta los datos nuevos al final de la lista

        Args:
            data_pack (list): Datos a insertar
        """

        for pack in data_pack:
            task = pack[0]
            data = pack[1]
            self.config_list.append([task, data])
            self.current_selection = [len(self.config_list) - 1]

    def change_modified(self, data_pack: list) -> None:
        """Modifica los datos de la línea seleccionada

        Args:
            data_pack (list): Lista de datos modificados
        """

        task = data_pack[0][0]
        data = data_pack[0][1]
        index = self.current_selection[0]
        self.config_list[index] = [task, data]

    def update_data(self) -> None:
        """Actualiza pantalla después de abrir"""

        self.tape_add()
        self.update_config_widget()
        self.update_tape_widgets()
        self.config_update_selection()
        self.tape1_update_selection()
        self.tape2_update_selection()
        self.modified_task = False

    def tape_add(self) -> None:
        """Genera líneas de tape a partir de la configuración"""

        self.tape1_list = []
        self.tape2_list = []
        self.current_config_line = 0

        for line in self.config_list:
            task = line[0]
            if task != "Inicio de programa":
                self.current_config_line += 1

            self.tasks_list[task].processor(self, line[1])
            self.tasks_list[task].button_switcher(self, line[1])
            self.tasks_list[task].generator(self, line[1])

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

    def config_clicked(self):
        """Ejecuta la selección de líneas de configuración"""

        self.current_widget = "config_widget"
        self.config_selected()

    def tape1_clicked(self):
        """Ejecuta la selección de líneas de tape 1"""

        self.current_widget = "tape1_widget"
        self.tape1_selected()

    def tape2_clicked(self):
        """Ejecuta la selección de líneas de tape 2"""

        self.current_widget = "tape2_widget"
        self.tape2_selected()

    def config_selected(self) -> None:
        """Devuelve las líneas seleccionadas de la configuración"""

        if self.current_widget == "config_widget":
            if selected_items := self.config_widget.selectedItems():
                config_lines = []
                config_lines.extend(
                    item.row() for item in selected_items if item.column() == 0
                )
                self.current_selection = sorted(list(set(config_lines)))

            self.tape1_update_selection()
            self.tape2_update_selection()

    def tape1_selected(self) -> None:
        """Obtiene los items seleccionados en tape2"""

        if self.current_widget == "tape1_widget":
            if selected_items := self.tape1_widget.selectedItems():
                self.items_selection(selected_items)

    def tape2_selected(self) -> None:
        """Obtiene los items seleccionados en tape2"""

        if self.current_widget == "tape2_widget":
            if selected_items := self.tape2_widget.selectedItems():
                self.items_selection(selected_items)

    def items_selection(self, selected_items):
        """Devuelve las líneas seleccionadas de la configuración

        Args:
            selected_items (list): Lista de items seleccionados
        """
        selected_list = []
        selected_list.extend(
            item.row() for item in selected_items if item.column() == 0
        )

        config_lines = [self.tape1_list[line][0] for line in selected_list]
        self.current_selection = sorted(list(set(config_lines)))

        if self.current_widget == "tape1_widget":
            self.config_update_selection()
            self.tape2_update_selection()
        elif self.current_widget == "tape2_widget":
            self.config_update_selection()
            self.tape1_update_selection()

    def config_update_selection(self) -> None:
        """Actualiza líneas seleccionadas en config"""

        all_items = [
            self.config_widget.item(index_number, 0)
            for index_number in range(len(self.config_list))
        ]

        indexes = self.current_selection
        items = [self.config_widget.item(index, 0) for index in indexes]

        self.items_selector(all_items, items, self.config_widget)

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

        self.items_selector(all_items, items, self.tape1_widget)

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

        self.items_selector(all_items, items, self.tape2_widget)

    def items_selector(self, all_items, items, widget):
        """Selecciona los items en el widget

        Args:
            all_items (list): Lista total de items en el widget
            items (list): Items a seleccionar
            widget (QTableWidget): Widget a seleccionar
        """
        with contextlib.suppress(AttributeError, IndexError):
            for item in all_items:
                item.setSelected(False)
            for item in items:
                item.setSelected(True)
            view = QAbstractItemView
            widget.scrollToItem(items[-1], view.PositionAtCenter)

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """
        if qKeyEvent.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
            self.config_modifier()
        elif qKeyEvent.key() == QtCore.Qt.Key_Home:
            self.home_position()
        elif qKeyEvent.key() == QtCore.Qt.Key_End:
            self.end_position()
        else:
            return

    # *
    # * Operaciones --------------------------------------------------------- *
    # *

    def helper(self, image: str) -> None:
        """Mostrar subventana"""
        if self.helper1:
            del self.helper1
        self.helper1 = Helper()
        self.helper1.show()
        image_load(self.helper1.lbl_image, image)

    def graph(self) -> None:
        """Mostrar subventana"""
        if self.graph1:
            del self.graph1
        self.graph1 = Graph()
        self.graph1.show()

    def header(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Header()
        self.subtask1.show()

    def free(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Free()
        # self.subtask1.show()

    def comment(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Comment()
        self.subtask1.show()

    def subrutine(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Subrutine()
        self.subtask1.show()

    def tool_call(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Tool_call()
        self.subtask1.show()

    def tool_close(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Tool_close()

    def spindle(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Spindle()
        self.subtask1.show()

    def end(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = End()

    def version(self) -> None:
        """Mostrar subventana"""
        self.subtask1 = Version()
        self.subtask1.show()


# ?
# ? Sub clases -------------------------------------------------------------- *
# ?

# ? ---------------------------------------------------------------------------
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

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """

        keyPressed(self, qKeyEvent)

    def closeEvent(self, event) -> None:
        window.modified_task = False
        if window.helper1:
            window.helper1.close()


# ? ---------------------------------------------------------------------------


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


class Version(QMainWindow, Ui_frm_version):
    """Ventana de información de versión

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica principal
        Ui_frm_version (_type_): Interfaz gráfica de la ventana
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


# ? ---------------------------------------------------------------------------


class Graph(QMainWindow, Ui_GraphWindow):
    """Ventana de ayuda para la tarea

    Args:
        QMainWindow (_type_): Clase de la interfaz gráfica principal
        Ui_GraphWindow (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.setupUi(self)

        self.vertical_moves = [0, 0, 0.1, 0.1]
        self.trasversal_moves = [0.05, 0.1, 0.15, 0.25]
        self.horizontal_moves = [0, 0, 0.15, 0.25]
        self.rapid_horizontal = [-0.05, 0]
        self.rapid_vertical = [-0.05, 0]

        self.construir_grafico()

    def construir_grafico(self):

        self.graph1_widget.setTitle("X - Z")
        self.graph1_widget.plot(
            self.horizontal_moves,
            self.vertical_moves,
            pen="blue",
        )
        self.graph1_widget.plot(
            self.rapid_horizontal,
            self.rapid_vertical,
            pen="gray",
        )
        # self.graph1_widget.setAspectLocked()
        self.graph1_widget.getPlotItem().hideAxis("bottom")
        self.graph1_widget.getPlotItem().hideAxis("left")

        self.graph2_widget.setTitle("Y - Z")
        self.graph2_widget.plot(self.horizontal_moves, self.trasversal_moves)
        # self.graph2_widget.setAspectLocked()
        self.graph2_widget.getPlotItem().hideAxis("bottom")
        self.graph2_widget.getPlotItem().hideAxis("left")

        # self.graph1_widget.setXLink(self.graph2_widget)

    def keyPressEvent(self, qKeyEvent) -> None:
        """Configurar comportamento de teclas presionadas

        Args:
            qKeyEvent (any): Evento de tecla presionada
        """

        keyPressed(self, qKeyEvent)


# ? ---------------------------------------------------------------------------


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

        image = "header.png"
        self.btn_help.clicked.connect(lambda: window.helper(image))

        self.cbx_mch.addItems(Lists.machine_list)
        self.cbx_cch.addItems(Lists.cutoff_list)
        self.cbx_wrk.addItems(Lists.work_offset_list)

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Prt": self.tbx_prt.text(),
            "Pgr": self.tbx_pgr.text(),
            "Dsc": self.tbx_dsc.text(),
            "Mch": self.cbx_mch.currentText(),
            "Dia": self.tbx_dia.text(),
            "Lgt": self.tbx_lgt.text(),
            "Chk": self.tbx_chk.text(),
            "Cch": self.cbx_cch.currentText(),
            "Wrk": self.cbx_wrk.currentText(),
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
            data["Dia"] = foper(data["Dia"])
            data["Lgt"] = foper(data["Lgt"])
            data["Chk"] = foper(data["Chk"])

        except ValueError:
            Messages.data_type_error(self)
            return

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()
        self.button_switcher(data)

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
            side (bool): Condición de lado del tape
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = header_gen(machine, data)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        window.modified_task = True
        prt, pgr, dsc, mch, dia, lgt, chk, cch, wrk = data.values()

        self.subtask1 = Header()
        self.subtask1.tbx_prt.setText(str(prt))
        self.subtask1.tbx_prt.setSelection(0, 100)
        self.subtask1.tbx_pgr.setText(str(pgr))
        self.subtask1.tbx_dsc.setText(str(dsc))
        self.subtask1.cbx_mch.setCurrentText(str(mch))
        self.subtask1.tbx_dia.setText(str(dia))
        self.subtask1.tbx_lgt.setText(str(lgt))
        self.subtask1.tbx_chk.setText(str(chk))
        self.subtask1.cbx_cch.setCurrentText(str(cch))
        self.subtask1.cbx_wrk.setCurrentText(str(wrk))
        self.subtask1.btn_save.setText("Actualizar")
        self.subtask1.show()

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.save_required = True
        window.current_side = "PRINCIPAL"
        window.current_machine = data["Mch"]
        window.part_name = data["Prt"]
        window.main_tape_number = data["Pgr"]
        window.tape_description = data["Dsc"]
        window.current_bar_diameter = float(data["Dia"])
        window.current_part_lenght = float(data["Lgt"])
        window.current_work_offset = data["Wrk"]
        window.swiss_back_machining = data["Chk"] > 0

        window.update_file_name()
        window.update_file_dir()
        window.load_main_title()

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.default_buttons_status()
        window.load_tape_conditions()

        for button_list in (
            window.main_buttons,
            window.turning_buttons,
            window.milling_buttons,
            window.drilling_buttons,
        ):
            for button in button_list:
                button.setEnabled(True)

        if window.current_machine != "Mazak":
            for button in window.plate_buttons:
                button.setEnabled(False)

        if window.current_machine == "Mazak":
            for button in window.turning_buttons:
                button.setEnabled(False)

        window.btn_header.setEnabled(False)
        window.btn_tool_close.setEnabled(False)


# ? ---------------------------------------------------------------------------


class Free(QMainWindow):
    """Espacio en blanco

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
            "Fre": " ",
        }

        self.validator(data)

    def validator(self, data: dict) -> None:
        """Validar datos ingresados por el usuario

        Args:
            data (dict): Diccionario de datos recopilados
        """

        self.converter(data)

    def converter(self, data: dict) -> None:
        """Convertir los datos al formato requerido

        Args:
            data (dict): Diccionario de datos recopilados
        """

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = free_gen(machine, data)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        pass

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.save_required = True

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.btn_free.setEnabled(True)

# ? ---------------------------------------------------------------------------


class Comment(Subtask_window, Ui_frm_comment):
    """Encabezado del programa

    Args:
        Subtask_window (_type_): Clase padre de la ventana
        Ui_frm_comment (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)

        image = "free.png"
        self.btn_help.clicked.connect(lambda: window.helper(image))

        self.cbx_sde.addItems(Lists.tape_sides)
        self.cbx_sde.setCurrentText(window.current_side)

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Com": self.tbx_com.text(),
            "Sde": self.cbx_sde.currentText(),
            "Blk": False,
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
            data["Com"] = ftext(data["Com"]) if data["Com"] != "" else ""

        except ValueError:
            Messages.data_type_error(self)
            return

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = comment_gen(machine, data)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        window.modified_task = True
        com, sde, blk = data.values()

        self.subtask1 = Comment()
        self.subtask1.tbx_com.setText(str(com))
        self.subtask1.tbx_com.setSelection(0, 100)
        self.subtask1.cbx_sde.setCurrentText(str(sde))
        self.subtask1.btn_save.setText("Actualizar")
        self.subtask1.show()

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.save_required = True
        window.current_comment = data["Com"]
        window.current_side = data["Sde"]

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.btn_comment.setEnabled(True)


# ? ---------------------------------------------------------------------------


class Subrutine(Subtask_window, Ui_frm_subrutine):
    """Encabezado del programa

    Args:
        Subtask_window (_type_): Clase padre de la ventana
        Ui_frm_subrutine (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)

        image = "subrutine.png"
        self.btn_help.clicked.connect(lambda: window.helper(image))

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Sub": self.tbx_sub.text(),
            "Rep": self.tbx_rep.text(),
            "Blk": False,
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
            data["Sub"] = ftext(data["Sub"]) if data["Sub"] != "" else ""
            data["Rep"] = foper(data["Rep"])
        except ValueError:
            Messages.data_type_error(self)
            return

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera lzas líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = subrutine_gen(machine, data)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        window.modified_task = True
        sub, rep, blk = data.values()

        self.subtask1 = Subrutine()
        self.subtask1.tbx_sub.setText(str(sub))
        self.subtask1.tbx_sub.setSelection(0, 100)
        self.subtask1.tbx_rep.setText(str(rep))
        self.subtask1.btn_save.setText("Actualizar")
        self.subtask1.show()

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.save_required = True
        window.current_side = "PRINCIPAL"

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.btn_subrutine.setEnabled(True)


# ? ---------------------------------------------------------------------------


class Tool_call(Subtask_window, Ui_frm_tool_call):
    """Encabezado del programa

    Args:
        Subtask_window (_type_): Clase padre de la ventana
        Ui_frm_tool_call (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)

        image = "tool.png"
        self.btn_help.clicked.connect(lambda: window.helper(image))

        self.cbx_typ.addItems(Lists.tool_list)
        self.cbx_sde.addItems(Lists.tape_sides)
        self.cbx_sde.setCurrentText(window.current_side)

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Tol": self.tbx_tol.text(),
            "Typ": self.cbx_typ.currentText(),
            "Dia": self.tbx_dia.text(),
            "Spc": self.tbx_spc.text(),
            "Sde": self.cbx_sde.currentText(),
            "Xin": self.tbx_xin.text(),
            "Yin": self.tbx_yin.text(),
            "Zin": self.tbx_zin.text(),
            "Blk": False,
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
            data["Tol"] = int(data["Tol"])
            data["Dia"] = foper(data["Dia"])
            data["Spc"] = ftext(data["Spc"]) if data["Spc"] != "" else ""
            data["Xin"] = foper(data["Xin"])
            data["Yin"] = foper(data["Yin"])
            data["Zin"] = foper(data["Zin"])
        except ValueError:
            Messages.data_type_error(self)
            return

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data2 = (
            " ",
            {
                "Fre": " ",
            },
        )
        data3 = (
            " ",
            {
                "Fre": "Rotación",
            },
        )
        data4 = [
            "        Comentario",
            {
                "Com": "DESCRIPCION",
                "Sde": data["Sde"],
                "Blk": False,
            },
        ]
        data5 = [
            "    Cerrar herramienta",
            {
                "Tol": data["Tol"],
                "Sde": data["Sde"],
                "Dia": window.current_bar_diameter,
                "Blk": False,
            },
        ]

        machine = window.current_machine
        if window.modified_task:
            data_pack = [data1]
        elif machine in ("B12", "A16", "K16", "E16", "OMNITURN"):
            data_pack = [data2, data1, data4, data5]
        else:
            data_pack = [data2, data1, data3, data4, data5]

        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
            side (bool): Condición de lado del tape
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = tool_call_gen(machine, data)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        window.modified_task = True
        tol, typ, dia, spc, sde, xin, yin, zin, blk = data.values()

        self.subtask1 = Tool_call()
        self.subtask1.tbx_tol.setText(str(tol))
        self.subtask1.tbx_tol.setSelection(0, 100)
        self.subtask1.cbx_typ.setCurrentText(str(typ))
        self.subtask1.tbx_dia.setText(str(dia))
        self.subtask1.tbx_spc.setText(str(spc))
        self.subtask1.cbx_sde.setCurrentText(str(sde))
        self.subtask1.tbx_xin.setText(str(xin))
        self.subtask1.tbx_yin.setText(str(yin))
        self.subtask1.tbx_zin.setText(str(zin))
        self.subtask1.btn_save.setText("Actualizar")
        self.subtask1.show()

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.save_required = True
        window.current_tool = int(data["Tol"])
        window.current_side = data["Sde"]

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.btn_tool_call.setEnabled(True)
        window.btn_tool_close.setEnabled(True)


# ? ---------------------------------------------------------------------------


class Tool_close(QMainWindow):
    """Cerrar herramienta

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
            "Tol": window.current_tool,
            "Sde": window.current_side,
            "Dia": window.current_bar_diameter,
            "Blk": False,
        }
        self.validator(data)

    def validator(self, data: dict) -> None:
        """Validar datos ingresados por el usuario

        Args:
            data (dict): Diccionario de datos recopilados
        """

        self.converter(data)

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

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape 1

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data["Tol"] = window.current_tool
        data["Sde"] = window.current_side
        data["Dia"] = window.current_bar_diameter

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = tool_close_gen(machine, data)
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

        window.btn_tool_close.setEnabled(False)

# ? ---------------------------------------------------------------------------


class Spindle(Subtask_window, Ui_frm_spindle):
    """Encabezado del programa

    Args:
        Subtask_window (_type_): Clase padre de la ventana
        Ui_frm_spindle (_type_): Interfaz gráfica de la ventana
    """

    def __init__(self) -> None:
        """Inicializar la clase"""

        super().__init__()
        self.task = find_task_name(window.tasks_list, __class__)

        image = "spindle.png"
        self.btn_help.clicked.connect(lambda: window.helper(image))

        self.cbx_rot.addItems(Lists.rotation_directions)
        self.cbx_sde.addItems(Lists.tape_sides)
        self.cbx_sde.setCurrentText(window.current_side)

    def collector(self) -> None:
        """Recopilar datos ingresado por el usuario"""

        data = {
            "Spd": self.tbx_spd.text(),
            "Rot": self.cbx_rot.currentText(),
            "Sde": self.cbx_sde.currentText(),
            "Blk": False,
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
            data["Spd"] = int(foper(data["Spd"]))

        except ValueError:
            Messages.data_type_error(self)
            return

        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaqueta datos recopilados y adicionales

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape

        Args:
            data (dict): Diccionario de datos recopilados
        """

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = spindle_gen(machine, data)
        window.tape_generator(lines, parameters)

    def modifier(self, data: dict) -> None:
        """Modifica las líneas de configuración

        Args:
            data (dict): Lista de datos de configuración
        """

        window.modified_task = True
        spd, rot, sde, blk = data.values()

        self.subtask1 = Spindle()
        self.subtask1.tbx_spd.setText(str(spd))
        self.subtask1.tbx_spd.setSelection(0, 100)
        self.subtask1.cbx_rot.setCurrentText(str(rot))
        self.subtask1.cbx_sde.setCurrentText(str(sde))
        self.subtask1.btn_save.setText("Actualizar")
        self.subtask1.show()

    def processor(self, data: dict) -> None:
        """Procesa las condiciones y datos de programa

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.save_required = True
        window.current_side = data["Sde"]

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """

        window.btn_spindle.setEnabled(True)

# ? ---------------------------------------------------------------------------


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
            "Blk": False,
        }
        self.packer(data)

    def packer(self, data: dict) -> None:
        """Empaquetar los datos a exportar

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data1 = (self.task, data)
        data_pack = [data1]
        window.config_add(data_pack)
        self.close()

    def generator(self, data: dict) -> None:
        """Genera las líneas del tape 1

        Args:
            data (dict): Diccionario de datos recopilados
        """

        data["Mch"] = window.current_machine

        parameters = window.get_parameters()
        machine = window.current_machine
        lines = end_gen(machine, data)
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
        self.save_required = True

    def button_switcher(self, data: dict) -> None:
        """Actualiza las condiciones de los botones

        Args:
            data (dict): Diccionario de datos recopilados
        """
        window.btn_end.setEnabled(False)


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
