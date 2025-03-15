import orjson
import tinydb
from requests_cache.backends import BaseCache, BaseStorage
from torm_storage.Torm import TormStorage

from torm_cache.TormSerializer import torm_serializer


class TORMCache(BaseCache):
    def __init__(self, autoremove=None, serializer=None, path=None, **kwargs):
        super().__init__(**kwargs)
        skwargs = {"serializer": serializer, **kwargs} if serializer else kwargs
        self.redirects = TORMDict(kind="redirects", autoremove=autoremove, path=path, **skwargs)
        self.responses = TORMDict(kind="responses", autoremove=autoremove, path=path,**skwargs)

class TORMDict(BaseStorage):
    def __init__(self, kind=None, autoremove=None, path=None, serializer=torm_serializer(), **kwargs):
        super().__init__(serializer=serializer, **kwargs)

        self._path = path
        self._autoremove = autoremove

        # TinyDB storage
        _db = tinydb.TinyDB(self._path, storage=TormStorage)
        self._db = _db.table(kind)
        self._Query = tinydb.Query()

    def __getitem__(self, key):
        # removal of {kind} data from database
        cache = self.deserialize(key, self.serialize(self._db.get(self._Query.key == key).get('data')))
        if cache.is_expired:
            self._db.remove(self._Query.key == key)

        return self.deserialize(key, self.serialize(self._db.get(self._Query.key == key).get('data')))

    def __setitem__(self, key, value):
        self._db.insert({"key": key, "data": orjson.loads(self.serialize(value).decode())})

    def __delitem__(self, key):
        self._db.remove(self._Query.key == key)

    def __iter__(self):
        return self._db.__iter__()

    def __len__(self):
        return self._db.__len__()

    def clear(self):
        self._db.truncate()
