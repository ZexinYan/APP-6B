import pymongo
from bson.objectid import ObjectId
from database.constant import DataBaseConstant


class TableBase:
    """
    property:
        first_name
        last_name
        address
        email
        phone
    """
    _client = None
    _table = None

    @staticmethod
    def table():
        raise NotImplementedError

    def find(self, condition=None, sort=None, skip=None, limit=None):
        _list = []
        table = self.table()
        if condition is None:
            find_result = table.find()
        else:
            find_result = table.find(condition)
        if sort is not None:
            find_result = find_result.sort(sort['key'], sort['value'])
        if skip is not None:
            find_result = find_result.skip(skip)
        if limit is not None:
            find_result = find_result.limit(limit)
        for each in find_result:
            each['_id'] = str(each['_id'])
            _list.append(each)
        return _list

    def insert_one(self, item):
        table = self.table()
        x = table.insert_one(item)
        return str(x.inserted_id)

    def update_one(self, _id, new_values):
        table = self.table()
        query = {'_id': ObjectId(_id)}
        new_values = {"$set": new_values}
        return table.update_one(query, new_values)

    def delete_one(self, _id):
        table = self.table()
        return table.delete_one({"_id": ObjectId(_id)})
