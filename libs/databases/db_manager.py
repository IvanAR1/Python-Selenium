from sqlalchemy import (
    URL,
    create_engine,  
    Connection, 
    text, 
    Engine,
    RootTransaction,
    MetaData
)
from libs.path.config_loader import env
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

class DBManager(DeclarativeBase):
    __abstract__ = True
    __bind_key__ = env("DB_DATABASE")
    urls:dict[URL] = {}
    engines:dict[Engine] = {}
    connections:dict[Connection] = {}
    transactions:dict[RootTransaction] = {}
    self_bind_keys = {}
    session:Session = None

    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        database = cls.__dict__.get("__bind_key__") or env("DB_DATABASE")
        if database:
            cls.add_urls(database=database)
            cls.add_engine(database)

    @classmethod
    def add_urls(
            cls,
            driver:str = (env("DB_CONNECTION") or env("DB_DRIVER")),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            username=env("DB_USERNAME"),
            password=env("DB_PASSWORD"),
            database=env("DB_DATABASE")
        ):
        if not cls.urls.get(database):
            cls.urls[database] = URL.create(
                driver, username, password, host, port, database=database
            )

    @classmethod
    def add_engine(cls, database):
        url = cls.urls.get(database)
        if database not in cls.engines:
            engine = create_engine(url)
            cls.engines[database] = engine
            cls.connections[database] = engine.connect()
            cls.metadata.create_all(bind = engine)
        if cls not in cls.self_bind_keys:
            cls.self_bind_keys[cls] = cls.engines[database]

    @classmethod
    def create_session(cls):
        if env("DB_DATABASE") not in cls.engines:
            cls.add_urls()
        if cls not in cls.self_bind_keys:
            cls.add_engine(env("DB_DATABASE"))
        session = sessionmaker()
        session.configure(binds=cls.self_bind_keys)
        cls.session = session()

    @classmethod    
    def query(cls, sql:str, params:dict={}, dictionary:bool=False, db_key:str=None):
        db_key = db_key or cls.__bind_key__
        connection = cls.connections.get(db_key)
        if connection:
            result = connection.execute(text(sql), params)
            if result.returns_rows and dictionary:
                return [row._asdict() for row in result]
            elif result.returns_rows:
                return result.fetchall()
            return {"lastId":result.lastrowid, "affecteds":result.rowcount, "_obj":result}
    
    @classmethod
    def begin(cls, db_key:str = None):
        db_key = db_key or cls.__bind_key__
        connection:Connection = cls.connections.get(db_key)
        if connection and cls.transactions.get(db_key) is None:
            cls.transactions[db_key] = connection.begin()

    @classmethod
    def commit(cls, db_key:str = None):
        db_key = db_key or cls.__bind_key__
        transaction:RootTransaction = cls.transactions.get(db_key)
        if transaction:
            transaction.commit()
            cls.transactions[db_key] = None

    @classmethod
    def rollback(cls, db_key:str = None):
        db_key = db_key or cls.__bind_key__
        transaction:RootTransaction = cls.transactions.get(db_key)
        if transaction:
            transaction.rollback()
            cls.transactions[db_key] = None

    @classmethod
    def _close(cls, db_key:str = None):
        db_key = db_key or cls.__bind_key__
        if db_key in cls.urls:
            cls.engines.pop(db_key, None)
            cls.connections.pop(db_key, None)
            cls.transactions.pop(db_key, None)
    
    @classmethod
    def _close_all(cls):
        for database, url in cls.urls.items():
            cls._close(database)
        cls.session.close_all()
        cls.urls = None
        cls.session = None