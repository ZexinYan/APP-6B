import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class RequestTable(TableBase):
    """
    property:
        player_id
        event_id
        request_time
        request_state
    """

    @staticmethod
    def table():
        if RequestTable._table is None:
            RequestTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            RequestTable._table = \
                RequestTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.REQUEST_TABLE]
        return RequestTable._table
