## aiomcache-multi

`aiomcache-multi` package is a minimal wrapper for asyncio-based memcached driver `aiomcache`.

While the original `aiomcache` client is capable of working with only one actual memcached backend server, `aiomcache-multi`
initializes with a list of backends and creates a corresponding number of aiomcache clients.

All well-known cache-related functions like `get`/`set` create a hash from a given cache key and choose a corresponding backend transparently.
`delete` method tries to remove cache on all the possible backends.

The default hashing algorithm is taken from the original `python-memcached` package.