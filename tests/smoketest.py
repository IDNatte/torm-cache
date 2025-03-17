import concurrent.futures as fu
import pprint
from datetime import timedelta

import requests_cache

from torm_cache.TormCache import TORMCache

backend = TORMCache(autoremove=False, path='./tests/dump/test.ndb')

r = requests_cache.CachedSession(backend=backend, expire_after=timedelta(minutes=5).seconds)

max = 500

def test(count):
    print(f"data : {count + 1}")
    url = f'https://httpbin.org/anything/data{count + 1}'
    c = r.get(url)
    # c = r.get('https://httpbin.org/absolute-redirect/2')
    #
    #
    print(r.cache.contains(url=url))

    if c.status_code == 200:
        data = c.json()
        return data


def main():
    with fu.ThreadPoolExecutor(max_workers=max/2) as threader:
        res = threader.map(test, range(max))


    pprint.pprint(list(res))


if __name__ == '__main__':
    main()
