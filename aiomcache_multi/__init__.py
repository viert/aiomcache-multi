import asyncio
import aiomcache
import binascii
import functools
from typing import List, Tuple


def server_hash_func(key):
    return (((binascii.crc32(key) & 0xffffffff) >> 16) & 0x7fff) or 1


def pick_and_retry(func):
    @functools.wraps(func)
    async def wrapper(self, key, *args, **kwargs):
        retry = 0
        while True:
            backend, key = self._get_backend(key, retry)
            try:
                data = await func(self, backend, key, *args, **kwargs)
                return data
            except:
                retry += 1
                if retry > Client.MAX_RETRIES:
                    raise
    return wrapper


class Client:

    MAX_RETRIES = 10

    def __init__(self, backends: List[Tuple], *, pool_size=2, pool_minsize=None, loop=None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self.backends = []
        for host, port in backends:
            backend = aiomcache.Client(host, port, pool_size=pool_size, pool_minsize=pool_minsize, loop=loop)
            self.backends.append(backend)

    def _get_backend(self, key: str, retry: int = 0):
        if not self.backends:
            return None, None

        if isinstance(key, tuple):
            serverhash, key = key
        else:
            serverhash = server_hash_func(key.encode('utf-8'))

        if retry:
            serverhash = str(serverhash) + str(retry)
            serverhash = server_hash_func(serverhash.encode('utf-8'))

        server = self.backends[serverhash % len(self.backends)]
        return server, key

    async def close(self):
        tasks = [backend.close() for backend in self.backends]
        await asyncio.gather(*tasks)

    @pick_and_retry
    async def get(self, backend, key: str, default=None):
        return await backend.get(key.encode(), default=default)

    @pick_and_retry
    async def set(self, backend, key: str, value: bytes, exptime=0):
        return await backend.set(key.encode(), value, exptime=exptime)

    async def multi_get(self, keys: List[str]) -> List[bytes]:
        tasks = [self.get(key) for key in keys]
        return await asyncio.gather(*tasks)

    async def delete(self, key):
        tasks = [backend.delete(key.encode()) for backend in self.backends]
        await asyncio.gather(*tasks)


__all__ = [Client, server_hash_func]
