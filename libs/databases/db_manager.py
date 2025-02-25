from sqlalchemy import (
    URL,
    create_engine,  
    Connection, 
    text, 
    Engine,
    RootTransaction,
    MetaData
)
from libs.path.loader import env
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

class DBManager(DeclarativeBase):
    """
    An class that manages databases using SqlAlchemy: <https://docs.sqlalchemy.org/en/20/>

    Inherince of:
        DeclarativeBase (SqlAlchemy.orm.DeclarativeBase): Base class used for declarative class definitions.

    Attributes:
        __abstract__ (bool): Indicates that the class is abstract and should not be instantiated directly. (please don't use it).
        __bind_key__ (str): The bind key used to identify the database.
        urls (dict[URL]): Dictionary of URLs for connecting to databases.
        engines (dict[Engine]): Dictionary of SQLAlchemy Engine instances.
        connections (dict[Connection]): Dictionary of active database connections.
        transactions (dict[RootTransaction]): Dictionary of active transactions.
        self_bind_keys (dict): Dictionary of bind keys for the class.
        session (Session): SQLAlchemy session instance.
        metadata (MetaData): SQLAlchemy MetaData instance with naming conventions.
    """
    __abstract__:bool = True
    __bind_key__:str = env("DB_DATABASE")
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
        """
        Initializes subclass by adding URLs and engines for the specified database.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init_subclass__(**kwargs)
        database = cls.__dict__.get("__bind_key__") or env("DB_DATABASE")
        if database:
            cls.add_urls(database=database)
            cls.add_engine(database)

    @classmethod
    def add_urls(
            cls,
            driver:str = (env("DB_CONNECTION") or env("DB_DRIVER")),
            host:str=env("DB_HOST"),
            port:str=env("DB_PORT"),
            username:str=env("DB_USERNAME"),
            password:str=env("DB_PASSWORD"),
            database:str=env("DB_DATABASE")
        ):
        """Add URLs for connecting to database.

        Args:
            driver (str, optional): Database driver. Defaults to ( env("DB_CONNECTION") or env("DB_DRIVER") ).
            host (_type_, optional): Database host. Defaults to env("DB_HOST").
            port (_type_, optional): Database port. Defaults to env("DB_PORT").
            username (_type_, optional): Database username. Defaults to env("DB_USERNAME").
            password (_type_, optional): Database password. Defaults to env("DB_PASSWORD").
            database (_type_, optional): Database name. Defaults to env("DB_DATABASE").
        """
        if not cls.urls.get(database):
            cls.urls[database] = URL.create(
                driver, username, password, host, port, database=database
            )

    @classmethod
    def add_engine(cls, database:str):
        """Adds an engine for the specified database.

        Args:
            database (str): Database name.
        """
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
        """
        Creates all SQLAlchemy sessions.
        """
        if env("DB_DATABASE") not in cls.engines:
            cls.add_urls()
        if cls not in cls.self_bind_keys:
            cls.add_engine(env("DB_DATABASE"))
        session = sessionmaker()
        session.configure(binds=cls.self_bind_keys)
        cls.session = session()

    @classmethod
    def query(cls, sql:str, params:dict={}, dictionary:bool=False, db_key:str=None) -> list|dict:
        """Executes a SQL Query. Review the docs in <https://docs.sqlalchemy.org/en/20/core/sqlelement.html> to correctly write a SQL Query.

        Args:
            sql (str): SQL Query string.
            params (dict, optional): Parameters for the SQL query. Defaults to {}.
            dictionary (bool, optional): Whether to return results as dictionaries. Defaults to False.
            db_key (str, optional): Bind key. Defaults to None.

        Returns:
            list|dict: Query results.
        """
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
        """Begins a new transaction.

        Args:
            db_key (str, optional): Bind key. Defaults to None.
        """
        db_key = db_key or cls.__bind_key__
        connection:Connection = cls.connections.get(db_key)
        if connection and cls.transactions.get(db_key) is None:
            cls.transactions[db_key] = connection.begin()

    @classmethod
    def commit(cls, db_key:str = None):
        """Commits the current transaction.

        Args:
            db_key (str, optional): Bind key. Defaults to None.
        """
        db_key = db_key or cls.__bind_key__
        transaction:RootTransaction = cls.transactions.get(db_key)
        if transaction:
            transaction.commit()
            cls.transactions[db_key] = None

    @classmethod
    def rollback(cls, db_key:str = None):
        """Rolls back the current transaction.

        Args:
            db_key (str, optional): Database key. Defaults to None.
        """
        db_key = db_key or cls.__bind_key__
        transaction:RootTransaction = cls.transactions.get(db_key)
        if transaction:
            transaction.rollback()
            cls.transactions[db_key] = None

    @classmethod
    def _close(cls, db_key:str = None):
        """Closes the connection to the specified database.

        Args:
            db_key (str, optional): Bind key. Defaults to None.
        """
        db_key = db_key or cls.__bind_key__
        if db_key in cls.urls:
            cls.engines.pop(db_key, None)
            cls.connections.pop(db_key, None)
            cls.transactions.pop(db_key, None)
    
    @classmethod
    def _close_all(cls):
        """
        Close all connections.
        """
        for database, _ in cls.urls.items():
            cls._close(database)
        cls.session.close_all()
        cls.urls = None
        cls.session = None