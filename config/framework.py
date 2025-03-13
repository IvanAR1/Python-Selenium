"""Modified framework arguments
Args:
    PATH_STRICT (bool): If pather manager is strict.
    EXCEL_ENGINE (str): Engine with which pandas works
    EXTENSION_LOADER (str): Extension file of environment (.env|.env.json)
    FORMAT_DATE (str): Formate date default.
    FORMAT_LOG_DATE (str): Formate date in folder log default.
"""
PATH_STRICT = False
EXCEL_ENGINE="openpyxl"
EXTENSION_LOADER=".env"
FORMAT_DATE="%Y-%m-%d"
FORMAT_LOG_DATE="%Y/%m"