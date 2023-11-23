import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class OrganizerTable(TableBase):
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
        if OrganizerTable._table is None:
            OrganizerTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            OrganizerTable._table = \
                OrganizerTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.ORGANIZER_TABLE]
        return OrganizerTable._table
