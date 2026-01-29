from .db_manager import database_manager


async def get_db():
    async for session in database_manager.get_session():
        yield session
