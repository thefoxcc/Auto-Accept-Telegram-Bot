import datetime
import motor.motor_asyncio
from config import Config
from helper.utils import send_log


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.date.today().isoformat(),
            welcome=None,
            leave = None,
            bool_welc = None,
            bool_leav = None
        )

    def approved_user(self, id):
        return dict(
            id = int(id)
        )
    async def set_welcome(self, user_id, welcome):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'welcome': welcome}})

    async def get_welcome(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('welcome', None)

    async def set_leave(self, user_id, leave):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'leave': leave}})

    async def get_leave(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('leave', None)

    async def set_bool_welc(self, user_id, bool_welc):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'bool_welc': bool_welc}})

    async def get_bool_welc(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bool_welc', None)

    async def set_bool_leav(self, user_id, boo_leav):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'bool_leav': boo_leav}})

    async def get_bool_leav(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bool_leav', None)

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def add_appro_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.approved_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)
            
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})


db = Database(Config.DB_URL, Config.DB_NAME)