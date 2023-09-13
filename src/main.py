import asyncio

from educon import EduconSession


async def main():
    try:
        session = EduconSession()
        await session.refresh_session()
        await session.start_polling()
    finally:
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
