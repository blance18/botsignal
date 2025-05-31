import aiosqlite

class DB:

    async def on_startup(self):
        self.con = await aiosqlite.connect("database/user.db")

        await self.con.execute(
            "CREATE TABLE IF NOT EXISTS users(verifed TEXT, user_id BIGINT PRIMARY KEY, lang TEXT)"
        )
        await self.con.execute("CREATE TABLE IF NOT EXISTS desc(ref TEXT)")

    async def get_ref(self) -> str:
        query = 'SELECT * FROM desc'
        result = await self.con.execute(query)
        row = await result.fetchone()
        if row is not None:
            return row[0]
        return None

    async def edit_ref(self, url: str) -> None:
        query = 'UPDATE desc SET ref = ? WHERE ref = ?'
        await self.con.execute(query, (url, await self.get_ref()))
        await self.con.commit()

    async def get_users_count(self) -> int:
        query = "SELECT COUNT(*) FROM users"
        result = await self.con.execute(query)
        return (await result.fetchone())[0]

    async def get_verified_users_count(self) -> int:
        query = "SELECT COUNT(*) FROM users WHERE verifed = 'verifed'"
        result = await self.con.execute(query)
        return (await result.fetchone())[0]

    async def register(self, user_id, language: str, verifed="0"):
        try:
            query = "INSERT INTO users(verifed, user_id, lang) VALUES(?, ?, ?)"
            await self.con.execute(query, (verifed, user_id, language))
            await self.con.commit()
        except aiosqlite.IntegrityError:
            pass

    async def update_verifed(self, user_id, verifed="verifed"):
        query = "UPDATE users SET verifed = ? WHERE user_id = ?"
        await self.con.execute(query, (verifed, user_id))
        await self.con.commit()

    async def get_user(self, user_id):
        ver = "verifed"
        query = 'SELECT * FROM users WHERE user_id = ? AND verifed = ?'
        result = await self.con.execute(query, (user_id, ver))
        return await result.fetchone()

    async def get_user_info(self, user_id):
        query = 'SELECT * FROM users WHERE user_id = ?'
        result = await self.con.execute(query, (user_id,))
        return await result.fetchone()

    async def get_users(self):
        query = "SELECT * FROM users"
        result = await self.con.execute(query)
        return await result.fetchall()

    async def update_lang(self, user_id, language: str):
        query = "UPDATE users SET lang = ? WHERE user_id = ?"
        await self.con.execute(query, (language, user_id))
        await self.con.commit()

    async def get_lang(self, user_id):
        query = "SELECT lang FROM users WHERE user_id = ?"
        result = await self.con.execute(query, (user_id,))
        row = await result.fetchone()
        if row is not None:
            return row[0]
        else:
            return None  # или значение по умолчанию, например, "en" для английского

DataBase = DB()
