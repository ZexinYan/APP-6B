import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class CommentTable(TableBase):
    """
    property:
        rating
        content
    """

    @staticmethod
    def table():
        if CommentTable._table is None:
            CommentTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            CommentTable._table = CommentTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.COMMENT_TABLE]
        return CommentTable._table
