import autoit
import threading
import pythoncom
import xlwings as xw
from libs.logs import api_logger
from typing import Callable, Union, List
from framework import FrameworkException

def excel_handle_popup(windows_titles:list, condition_while:Callable[[], bool], button_to_click:Callable[[], bool]):
    """Handles excel popups dynamically until told to stop.

    Args:
        windows_titles (list): Popups names list.
        condition_while (Callable[[], bool]): Condition that while validate if true.
        button_to_click (Callable[[], bool]): Action to click.

    Raises:
        FrameworkException: If 'condition_while' or 'button_to_click' is not Callable or others Exceptions.
    """
    pythoncom.CoInitialize()
    try:
        api_logger.info(f"\Searching windows {windows_titles}")
        while condition_while():
            for win_title in windows_titles:
                if autoit.win_exists(win_title):
                    api_logger.info(f"\Window '{win_title}' found.")
                    autoit.win_activate(win_title)
                    button_to_click()
    except (TypeError, Exception) as e:
        raise FrameworkException(f"An error ocurred in excel handle popup: {e}")
    finally:
        pythoncom.CoUninitialize()

def execute_macro(file_path:str, macro_name:str, thread_callable:Callable[[], List[Union[threading.Event, threading.Thread]]] = None):
    """Execute macros.

    Args:
        file_path (str): Excel file path location
        macro_name (str): Macro name
        thread_callable (Callable[[], List[Union[threading.Event, threading.Thread]]], optional): Returned [threading.Event, threading.Thread]. Defaults to None.
    """
    try:
        with xw.App(visible=False) as app:
            # Abrir el archivo
            workbook = app.books.open(file_path)

            # Iniciar hilo para manejar ventanas emergentes
            if thread_callable is not None:
                stop_event, popup_thread = thread_callable()
            try:
                # Ejecutar la macro
                workbook.macro(macro_name)()
                api_logger.info(f"Macro ejecutada correctamente en {file_path}")
            except Exception as e:
                api_logger.error(f"Error al ejecutar la macro en {file_path}: {e}")
            finally:
                # Detener el hilo de manejo de ventanas emergentes
                if thread_callable is not None:
                    if isinstance(stop_event, threading.Event):
                        stop_event.set()
                    if isinstance(popup_thread, threading.Thread):
                        popup_thread.join()
                # Guardar y cerrar el archivo
                workbook.save()
                workbook.close()
    except Exception as e:
        api_logger.error(f"Error procesando archivo {file_path}: {e}")
    

def execute_macro_with_notifications(file_path:str, macro_name:str, windows_titles:list, button_to_click:str = "{ENTER}"):
    """Execute a macro with notifications. 

    Args:
        file_path (str): Excel file path location
        macro_name (str): Macro name
        windows_titles (list): Popups names list.
        button_to_click (str, optional): Button str to click. Defaults to "{ENTER}".
    """
    def notification_thread():
        stop_event = threading.Event()
        popup_thread = threading.Thread(target=excel_handle_popup, args=(windows_titles, lambda: not stop_event.is_set(), lambda: autoit.send(button_to_click)))
        popup_thread.start()
        return stop_event, popup_thread
    execute_macro(file_path, macro_name, notification_thread)