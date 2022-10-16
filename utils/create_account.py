import asyncio
from pprint import pprint

from telegraph.aio import Telegraph


async def main():
    telegraph = Telegraph()
    print(await telegraph.create_account(short_name='sarafan'))

    response = await telegraph.create_page(
        'Hey',
        html_content='<p>Hello, world!</p>',
    )
    pprint(response['url'])
    print('asd')


asyncio.run(main())