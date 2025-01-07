from mysql import connector 
from ..path.config_loader import env

class MySQLManager:
    connection:connector.MySQLConnection = None

    @staticmethod
    def conn()->connector.MySQLConnection:
        if(env("DB_CONNECTION") == "mysql"):
            host = env("DB_HOST");
            port = env("DB_PORT");
            database = env("DB_DATABASE");
            user = env("DB_USERNAME");
            password = env("DB_PASSWORD");
            conn = connector.connect(host=host, port=port, user=user, password=password, database=database);
            return conn;

    @staticmethod
    def query(sql:str, params=(), dictionary:bool=False):
        if MySQLManager.connection != None:
            cursor = MySQLManager.connection.cursor(dictionary=dictionary);
            cursor.execute(sql, params);
            return cursor

    @staticmethod
    def beginTransaction():
        if MySQLManager.connection != None:
            MySQLManager.connection.start_transaction();

    @staticmethod
    def commit():
        if MySQLManager.connection != None:
            MySQLManager.connection.commit();

    @staticmethod
    def rollback():
        if MySQLManager.connection != None:
            MySQLManager.connection.rollback();