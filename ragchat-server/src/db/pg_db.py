import os
import ssl
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


database_url = os.getenv('DATABASE_URL')


def get_db_url() -> str:
    return database_url


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    get_db_url(),
    pool_size=10,
    pool_recycle=3600,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={
        "ssl": ctx,
        "server_settings": {
            "jit": "off",
        }
    }
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = async_session()
        yield db
    except Exception as e:
        # 记录日志或进行其他处理
        print(f"数据操作错误:{e}")
        if db and db.in_transaction():
            await db.rollback()
            raise
    finally:
        if db:
            await db.close()
