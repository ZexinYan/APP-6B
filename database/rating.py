import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class RatingTable(TableBase):
    """
    property:
        rater
        time
        event
    """

    @staticmethod
    def table():
        if RatingTable._table is None:
            RatingTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            RatingTable._table = RatingTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.RATING_TABLE]
        return RatingTable._table
