import pymongo
from database.constant import DataBaseConstant
from database.table_base import TableBase


class BankAccountTable(TableBase):
    """
    property:
        user_id
        holder_name
        account_number
        bank_name
    """

    @staticmethod
    def table():
        if BankAccountTable._table is None:
            BankAccountTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            BankAccountTable._table = \
                BankAccountTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.BANK_ACCOUNT_TABLE]
        return BankAccountTable._table
