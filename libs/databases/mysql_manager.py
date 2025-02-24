from mysql import connector
from ..path.loader import env
from mysql.connector.cursor import CursorBase

class MySQLManager:
    """
    A class that manage ony MySQL databases.

    Attributes:
        connection (connector.MySQLConnection): Active connection.
    """
    connection:connector.MySQLConnection = None

    @staticmethod
    def conn()->connector.MySQLConnection:
        """Create a connection to MySQL database.

        Returns:
            connector.MySQLConnection: Connection to MySQL database.
        """
        if(env("DB_CONNECTION") == "mysql"):
            host = env("DB_HOST")
            port = env("DB_PORT")
            database = env("DB_DATABASE")
            user = env("DB_USERNAME")
            password = env("DB_PASSWORD")
            conn = connector.connect(host=host, port=port, user=user, password=password, database=database)
            return conn

    @staticmethod
    def query(sql:str, params=(), dictionary:bool=False) -> CursorBase|list|dict|any:
        """Execute a SQL Query.

        Args:
            sql (str): SQL Query string.
            params (tuple, optional): Parameters for the SQL query. Defaults to ().
            dictionary (bool, optional): _description_. Defaults to False.

        Returns:
            CursorBase|list|dict|any: Query results.
        """
        if MySQLManager.connection is not None:
            cursor = MySQLManager.connection.cursor(dictionary=dictionary)
            cursor.execute(sql, params)
            return cursor

    @staticmethod
    def begin():
        """Begins a new transaction.
        """
        if MySQLManager.connection is not None:
            MySQLManager.connection.start_transaction()

    @staticmethod
    def commit():
        """Commits the current transaction.
        """
        if MySQLManager.connection is not None:
            MySQLManager.connection.commit()

    @staticmethod
    def rollback():
        """Rolls back the current transaction.
        """
        if MySQLManager.connection is not None:
            MySQLManager.connection.rollback()