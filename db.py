import aiosqlite

class DB:

    async def on_startup(self):
        self.con = await aiosqlite.connect("database/user.db")

        await self.con.execute(
            "CREATE TABLE IF NOT EXISTS users(verifed TEXT, user_id BIGINT PRIMARY KEY, lang TEXT)"
        )
        await self.con.execute("CREATE TABLE IF NOT EXISTS desc(ref TEXT)")

    async def get_ref(self) -> str:
        result = await self.con.execute('SELECT * FROM desc')
        row = await result.fetchone()
        return row[0] if row else None

    async def edit_ref(self, url: str) -> None:
        await self.con.execute('UPDATE desc SET ref = ? WHERE ref = ?', (url, await self.get_ref()))
        await self.con.commit()

    async def get_users_count(self) -> int:
        result = await self.con.execute("SELECT COUNT(*) FROM users")
        return (await result.fetchone())[0]

    async def get_verified_users_count(self) -> int:
        result = await self.con.execute("SELECT COUNT(*) FROM users WHERE verifed = 'verifed'")
        return (await result.fetchone())[0]

    async def register(self, user_id, language: str, verifed="0"):
        try:
            await self.con.execute(
                "INSERT INTO users(verifed, user_id, lang) VALUES(?, ?, ?)",
                (verifed, user_id, language)
            )
            await self.con.commit()
        except aiosqlite.IntegrityError:
            pass

    async def update_verifed(self, user_id, verifed="verifed"):
        await self.con.execute(
            "UPDATE users SET verifed = ? WHERE user_id = ?",
            (verifed, user_id)
        )
        await self.con.commit()

    async def get_user(self, user_id):
        result = await self.con.execute(
            "SELECT * FROM users WHERE user_id = ? AND verifed = 'verifed'",
            (user_id,)
        )
        return await result.fetchone()

    async def get_user_info(self, user_id):
        result = await self.con.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return await result.fetchone()

    async def get_users(self):
        result = await self.con.execute("SELECT * FROM users")
        return await result.fetchall()

    async def update_lang(self, user_id, language: str):
        await self.con.execute("UPDATE users SET lang = ? WHERE user_id = ?", (language, user_id))
        await self.con.commit()

    async def get_lang(self, user_id):
        result = await self.con.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        row = await result.fetchone()
        return row[0] if row else None

DataBase = DB()
