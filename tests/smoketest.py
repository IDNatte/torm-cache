# import datetime
# import pathlib

# import requests_cache

# from torm_cache.TormCache import TORMCache

# DEBUG_DATABASE = pathlib.Path('tests/dump/test.ndb')

# backend = TORMCache(path=DEBUG_DATABASE, autoremove=True)
# r = requests_cache.CachedSession(backend=backend, expire_after=1)

# def test():
#     print(datetime.timedelta(minutes=1).seconds)
#     c = r.get('https://httpbin.org/get')
#     # c = r.get('https://web.tapinkab.go.id')
#     # print(len())
#     # for x in r.cache.responses:
#     #     print(x)

#     if c.status_code == 200:
#         json_data = c.json()
#         print(json_data)
#         # r.cache.clear()


# if __name__=="__main__":
#     test()


import concurrent.futures as fu
import pprint
from datetime import timedelta

import requests_cache

from torm_cache.TormCache import TORMCache

backend = TORMCache(autoremove=True, path='./dump/test.ndb')

r = requests_cache.CachedSession(backend=backend, expire_after=timedelta(minutes=5).seconds)

max = 100

def test(count):
    print(count)
    c = r.get(f'https://httpbin.org/anything/{count + 1}')
    if c.status_code == 200:
        data = c.json()
        return data


def main():
    with fu.ThreadPoolExecutor(max_workers=5) as threader:
        threader.map(test, range(max))


    # pprint.pprint(list(res))


if __name__ == '__main__':
    main()
