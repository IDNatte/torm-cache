import datetime
import pathlib

import requests_cache

from torm_cache.TormCache import TORMCache

DEBUG_DATABASE = pathlib.Path('tests/dump/test.ndb')

backend = TORMCache(path=DEBUG_DATABASE, autoremove=True)
r = requests_cache.CachedSession(backend=backend, expire_after=1)

def test():
    print(datetime.timedelta(minutes=1).seconds)
    c = r.get('https://httpbin.org/get')
    # c = r.get('https://web.tapinkab.go.id')
    # print(len())
    # for x in r.cache.responses:
    #     print(x)

    if c.status_code == 200:
        json_data = c.json()
        print(json_data)
        # r.cache.clear()


if __name__=="__main__":
    test()
