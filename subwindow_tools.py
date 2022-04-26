from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from pathlib import Path


def find_task_name(task_list: dict, class_name: object) -> str:
    """Buscar nombre de la tarea según la clase

    Args:
        task_list (dict): Lista de tareas
        class_name (object): Nombre de la clase

    Returns:
        str: Nombre de la tarea
    """

    keys_list = list(task_list.keys())
    values_list = list(task_list.values())
    position = values_list.index(class_name)

    return keys_list[position]


def keyPressed(self, qKeyEvent) -> None:
    """Configurar comportamento de teclas presionadas

    Args:
        qKeyEvent (any): Evento de tecla presionada
    """
    if qKeyEvent.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
        self.focusNextChild()
    elif qKeyEvent.key() == QtCore.Qt.Key_Escape:
        self.close()
    else:
        return


def absPath(file: str) -> str:
    """Verifica el directorio del archivo

    Args:
        file (str): Archivo a verificar

    Returns:
        str: Directorio del archivo
    """
    return str(Path(__file__).parent.absolute() / file)


def image_load(label: str, image: str) -> None:
    """Carga una imagen en una etiqueta

    Args:
        label (str): Etiqueta a rellenar
        image (str): Imagen a cargar
    """
    image = QPixmap(absPath(f"Resources/{image}"))
    label.setPixmap(image)
    label.setScaledContents(True)
