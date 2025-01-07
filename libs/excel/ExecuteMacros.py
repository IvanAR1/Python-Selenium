import autoit
import threading
import pythoncom
import xlwings as xw
from libs.logs import api_logger
from collections.abc import Callable

def excel_handle_popup(windows_titles:list, condition_while:Callable, button_to_click:str):
    """Maneja ventanas emergentes dinámicamente hasta que se indique detenerse."""
    pythoncom.CoInitialize()
    try:
        api_logger.info(f"\rBuscando ventanas {windows_titles}")
        while condition_while():
            for win_title in windows_titles:
                if autoit.win_exists(win_title):
                    api_logger.info(f"\nVentana '{win_title}' encontrada.")
                    autoit.win_activate(win_title)
                    autoit.send(button_to_click)
    except Exception as e:
        api_logger.error(f"Error en handle_popup: {e}")
    finally:
        pythoncom.CoUninitialize()

def execute_macro(file_path:str, macro_name:str, thread_callable:Callable[[],str] = None):
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
                    stop_event.set()
                    popup_thread.join()

                # Guardar y cerrar el archivo
                workbook.save()
                workbook.close()
    except Exception as e:
        api_logger.error(f"Error procesando archivo {file_path}: {e}")
    

def execute_macro_with_notifications(file_path:str, macro_name:str, windows_titles:list, button_to_click:str = "{ENTER}"):
    def notification_thread():
        stop_event = threading.Event()
        popup_thread = threading.Thread(target=excel_handle_popup, args=(windows_titles, lambda: not stop_event.is_set(), button_to_click))
        popup_thread.start()
        return stop_event, popup_thread
    execute_macro(file_path, macro_name, notification_thread)