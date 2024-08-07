import asyncio
from crest_api.crest import CRest

from environs import Env

env = Env()
env.read_env(override=True)

domain = env.str("domain")
format = env.str("format")


async def get_contacts():
    bx24_client = CRest(domain, "json", "")

    print(
        await bx24_client.call(
            method='crm.contact.list',
            format=format,
            params={
                'FILTER': {
                    '>DATE_CREATE': '2022-01-01'
                },
                'SELECT': [
                    'NAME',
                    'LAST_NAME',
                    'EMAIL'
                ]
            }
        )
    )


async def add_contacts():
    bx24_client = CRest(domain, "json", "")

    contacts = []
    for i in range(1000):
        contacts.append(
            {
                "NAME": f"new{i}",
                "LAST_NAME": f"new{i}",
                "EMAIL": f"test{i}",
                "COMMENTS": f"test{i}"
            }
        )
    for contact in contacts:
        print(
            await bx24_client.call(
                method="crm.contact.add",
                format=format,
                params={
                    "fields": contact
                }
            )
        )


async def add_contacts_batch():
    bx24_client = CRest(domain, "json", "")
    print()
    contacts = []
    for i in range(1000):
        contacts.append(
            {
                "NAME": f"new{i}",
                "LAST_NAME": f"new{i}",
                "EMAIL": f"test{i}",
                "COMMENTS": f"test{i}"
            }
        )
    calls = []
    for contact in contacts:
        calls.append(
            {
                "method": "crm.contact.add",
                "params": {
                    "fields": contact
                }
            }
        )
    await bx24_client.batch_call(calls)


async def main():
    await add_contacts_batch()

asyncio.run(main())
