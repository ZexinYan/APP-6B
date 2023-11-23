import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class PlayerTable(TableBase):
    """
    property:
        first_name
        last_name
        address
        email
        password
        phone
    """

    @staticmethod
    def table():
        if PlayerTable._table is None:
            PlayerTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            PlayerTable._table = PlayerTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.PLAYER_TABLE]
        return PlayerTable._table
