from sqlalchemy import (
    URL,
    create_engine,  
    Connection, 
    text, 
    Engine,
    RootTransaction,
)
from libs.path.config_loader import env
from sqlalchemy.orm import declarative_base, sessionmaker, Session

BASE = declarative_base()

class DBManager(BASE):
    __abstract__ = True
    engine:Engine = None
    session:Session = None
    connection:Connection = None
    transaction:RootTransaction = None

    @classmethod
    def conn(
            self,
            driver:str = (env("DB_CONNECTION") or env("DB_DRIVER")),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            username=env("DB_USERNAME"),
            password=env("DB_PASSWORD"),
            database=env("DB_DATABASE")
        ):
        url = URL.create(
            driver, host=host, port=port, username=username, password=password, database=database
        )
        self.engine = create_engine(url)
        self.session = sessionmaker(bind=self.engine, autoflush=False)()
        self.connection = self.engine.connect()
        BASE.metadata.create_all(bind=self.engine)

    @classmethod    
    def query(self, sql:str, params:dict={}, dictionary:bool=False):
        result = self.connection.execute(text(sql), params)
        if result.returns_rows and dictionary:
            return [row._asdict() for row in result]
        elif result.returns_rows:
            return result.fetchall()
        return {"lastId":result.lastrowid, "affecteds":result.rowcount, "_obj":result}
    
    @classmethod
    def begin(self):
        if self.transaction is None:
            self.transaction = self.connection.begin()

    @classmethod
    def commit(self):
        if self.transaction:
            self.transaction.commit()
            self.transaction = None

    @classmethod
    def rollback(self):
        if self.transaction:
            self.transaction.rollback()
            self.transaction = None

    @classmethod
    def to_dict(self, obj):
        return {key:value for key, value in obj.__dict__.items() if not key.startswith("_")}

    @classmethod
    def _close(self):
        self.session.close()