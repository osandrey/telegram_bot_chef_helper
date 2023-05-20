import asyncio
import ssl

import certifi
import requests
import random
import platform
import aiohttp
from time import time
from concurrent.futures import ThreadPoolExecutor
from aiofile import async_open, AIOFile, LineReader
from aiopath import AsyncPath
from aioshutil import copyfile
#
# fake_users = [
#     {'id': 1, 'name': 'April Murphy', 'company': 'Bailey Inc', 'email': 'shawnlittle@example.org'},
#     {'id': 2, 'name': 'Emily Alexander', 'company': 'Martinez-Smith', 'email': 'turnerandrew@example.org'},
#     {'id': 3, 'name': 'Patrick Jones', 'company': 'Young, Pruitt and Miller', 'email': 'alancoleman@example.net'}
# ]
#
#
# async def get_user_async(uid: int) -> dict:
#     await asyncio.sleep(0.5)
#     user, = list(filter(lambda user: user["id"] == uid, fake_users))
#     return user
#
#
# async def main():
#     r = []
#     for i in range(1, 4):
#         r.append(get_user_async(i))
#     return await asyncio.gather(*r)
#
#
# if __name__ == '__main__':
#     start = time()
#     result = asyncio.run(main())
#     for r in result:
#         print(r)
#     print(time() - start)

#
# async def get_r_num():
#     print('-- -- --start task')
#     await asyncio.sleep(1)
#     print('-- -- --task finished')
#     return random.random()
#
# async def main():
#     task = asyncio.create_task(get_r_num(), name='ANDRII')
#     print('Task scheduled successfully')
#     await task
#     print(f'Result is: {task.result()}')
#
# if __name__ == '__main__':
#     for i in range(1, 5):
#         asyncio.run(main())
#
#
#
# def blocks(n):
#     counter = n
#     start = time()
#     while counter > 0:
#         counter -= 1
#     return time() - start
#
#
# async def monitoring():
#     while True:
#         await asyncio.sleep(2)
#         print(f'Monitoring {time()}')
#
# async def run_blocking_tasks(executor, n):
#     loop = asyncio.get_event_loop()
#     print('Waiting for executor tasks')
#     result = await loop.run_in_executor(executor, blocks, n)
#     return result
#
# async def main():
#     asyncio.create_task(monitoring())
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         futures = [run_blocking_tasks(executor,n) for n in [50000000, 60000000]]
#         result = await asyncio.gather(*futures)
#         return result
#
# if __name__ == '__main__':
#     result = asyncio.run(main())
#     for i in result:
#         print(i)


#
#
# urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com']
#
#
# def preview_fetch(url):
#     r = requests.get(url)
#     return url, r.text[:150]
#
# async def preview_fetch_async():
#     loop = asyncio.get_running_loop()
#
#     with ThreadPoolExecutor(max_workers=3) as pool:
#         futures = [loop.run_in_executor(pool, preview_fetch, url) for url in urls]
#         result = await asyncio.gather(*futures, return_exceptions=True)
#         return result
#
# if __name__ == '__main__':
#     start = time()
#     r = asyncio.run(preview_fetch_async())
#     print(r)
#     print(time() - start)
#
# async def main():
#     async with async_open('TEST.txt', 'w+') as async_file:
#         await async_file.write('Hello ')
#         await async_file.write('world\n')
#         await async_file.write('Hello from async world' + '\n')
#         await async_file.write('Bye-Bye' + '\n')
#
# async def read():
#     async with async_open('TEST.txt', 'r') as async_file:
#         print(await async_file.read(length=-1))
#
# async def read_async_for():
#     async with async_open('TEST.txt', 'r') as afp:
#         async for line in afp:
#             print(f'ASYNC FOR METHOD: {line}')
#
#
#
# async def file_line_reader():
#     async with AIOFile('TEST.txt', 'r') as afp:
#         async for line in LineReader(afp):
#             print('LINE READER METHOD:' + line)
#
#
# async def async_path_func():
#     '''
#     Ця функція перевіряє наявність файлу в корневій папці
#     '''
#     async_path = AsyncPath('test.txt')
#     print(await async_path.exists())
#     print(await async_path.is_file())
#     print(await async_path.is_dir())
#
#
# async def aio_shutil_func():
#     '''Ця функція створить папку (new_path) і скопіює до неї наш файл'''
#     a_path = AsyncPath('test.txt')
#     if await a_path.exists():
#         new_path = AsyncPath('async_tests')
#         await new_path.mkdir(exist_ok=True, parents=True)
#         await copyfile(a_path, new_path / a_path)

# async def async_http_req():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://python.org') as response:
#
#             print(f'Status = {response.status}')
#             print('Content-type', response.headers['content-type'])
#
#             html = await response.text()
#             print(f'Body of web: {html[:20]} . . . ')

# if __name__ == '__main__':
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(main())
    # asyncio.run(main())
    # asyncio.run(read())
    # asyncio.run(read_async_for())
    # asyncio.run(file_line_reader())
    # asyncio.run(async_path_func())
    # asyncio.run(aio_shutil_func())

import platform

import aiohttp
import asyncio


async def client_func():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5', ssl_context=ssl_context) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            return result

async def get_server_response():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5', ssl_context=ssl_context) as response:
            print('Status: ', response.status)
            print('Content-type: ', response.headers['Content-Type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            # result = await response.read()
            # result = await response.text()
            result = await response.json()
            return result

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    client = asyncio.run(client_func())
    print(client)
    serv = asyncio.run(get_server_response())
    print(serv)

