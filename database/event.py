import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class EventTable(TableBase):
    """
    property:
        name
        time
        desc
        location
        category
    """

    @staticmethod
    def table():
        if EventTable._table is None:
            EventTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            EventTable._table = EventTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.EVENT_TABLE]
        return EventTable._table
