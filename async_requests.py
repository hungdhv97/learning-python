import asyncio

import aiohttp
import aioredis

# Danh sách các endpoint
endpoints = [
    'https://jsonplaceholder.typicode.com/posts/1',
    'https://jsonplaceholder.typicode.com/posts/2',
    'https://jsonplaceholder.typicode.com/posts/3',
    'https://jsonplaceholder.typicode.com/posts/4',
    'https://jsonplaceholder.typicode.com/posts/5'
]


async def fetch(session, url, redis):
    cache_key = f'cache:{url}'
    cached_response = await redis.get(cache_key)
    if cached_response:
        print(f'Cache hit for {url}')
        return cached_response

    print(f'Cache miss for {url}')
    async with session.get(url) as response:
        response_text = await response.text()
        await redis.set(cache_key, response_text)
        await redis.expire(cache_key, 10)
        return response_text


async def main():
    async with aiohttp.ClientSession() as session:
        redis = aioredis.from_url('redis://:password@localhost:6379', decode_responses=True)
        tasks = [fetch(session, url, redis) for url in endpoints]
        responses = await asyncio.gather(*tasks)
        await redis.close()


if __name__ == '__main__':
    asyncio.run(main())
