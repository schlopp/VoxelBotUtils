from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .model import DatabaseWrapper, DatabaseTransaction


class DatabaseConfig(typing.TypedDict):
    enabled: bool
    host: str
    port: int
    database: str
    user: str
    password: str


class UserDatabaseConfig(DatabaseConfig):
    enabled: bool


class DriverFetchConnection(typing.Protocol):

    async def fetch(self):
        raise NotImplementedError()


class DriverExecuteConnection(typing.Protocol):

    async def execute(self):
        raise NotImplementedError()


DriverConnection = typing.Union[DriverFetchConnection, DriverExecuteConnection]


class DriverPool(typing.Protocol):

    async def acquire(self) -> DriverConnection:
        raise NotImplementedError()

    async def release(self, connection: DriverConnection) -> None:
        raise NotImplementedError()


class DriverWrapper(typing.Protocol):

    @staticmethod
    async def create_pool(config: DatabaseConfig) -> DriverPool:
        """
        Connect to your database driver using the given config.
        """

        ...

    @staticmethod
    async def get_connection(dbw: typing.Type[DatabaseWrapper]) -> DatabaseWrapper:
        """
        Get a connection from the database pool and return a wrapper
        around the given connection.
        """

        ...

    @staticmethod
    async def release_connection(dbw: DatabaseWrapper) -> None:
        """
        Release the connection back into the pool.
        """

        ...

    @classmethod
    def transaction(cls, dbw: DatabaseWrapper, *, commit_on_exit: bool = True):
        """
        Make a transaction instance with the connection's current instance.
        """

        return DatabaseTransaction(cls, dbw, commit_on_exit=commit_on_exit)

    @staticmethod
    async def start_transaction(dbw: DatabaseTransaction) -> None:
        """
        Start a transaction from the transaction wrapper.
        """

        ...

    @staticmethod
    async def commit_transaction(dbw: DatabaseTransaction) -> None:
        """
        Commit the transaction from the wrapper.
        """

        ...

    @staticmethod
    async def rollback_transaction(dbw: DatabaseTransaction) -> None:
        """
        Rollback the commits from the transaction.
        """

        ...

    @staticmethod
    async def fetch(dbw: DatabaseTransaction, sql: str, *args) -> typing.List[typing.Any]:
        """
        Run some SQL in your database
        """

        ...
