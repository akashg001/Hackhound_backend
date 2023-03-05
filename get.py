# import asyncpg
#
# async def get_database_pool():
#     return await asyncpg.create_pool(
#         host="localhost",
#         port=26257,
#         user="root",
#         database="mydatabase",
#         password=None,
#         sslmode="disable",
#     )
#
#     pool = await get_database_pool()