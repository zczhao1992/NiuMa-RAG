import os

from sqlalchemy import delete, select, UUID, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.chunk import Chunk
from src.utils.sql_template_manager import SQLTemplateManager
from sqlalchemy import text


class ChunkDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Chunk, primary_key="uuid")
        self.sql_template_manager = SQLTemplateManager(
            os.path.dirname(__file__))

    async def get_by_file_id(self, file_id: UUID):
        result = await self.db.execute(
            select(Chunk)
            .where(Chunk.file_id == file_id)
            .order_by(Chunk.index)
        )
        return result.scalars().all()

    async def get_chunks_by_ids(self, chunk_ids: list[UUID]):
        if not chunk_ids:
            return []
        stmt = select(Chunk).where(Chunk.uuid.in_(chunk_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def batch_update_status_by_uuids(self, uuids: list[UUID], new_status: int):
        """
        批量更新 chunk 的状态
        """
        if not uuids:
            return

        stmt = (
            update(Chunk)
            .where(Chunk.uuid.in_(uuids))
            .values(status=new_status)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete_chunks_by_file_id(self, file_id: str):

        stmt = delete(Chunk).where(Chunk.file_id == file_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def query_embedding_chunks(self):
        try:
            # 确保 db 以正确初始化
            if not self.db:
                return []
            sql = self.sql_template_manager.render_sql(
                'sql/chunk_query.sql.j2')
            result = await self.db.execute(text(sql))

            if result is None:
                return []

            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]

            return rows
        except FileNotFoundError:
            print(f"错误: sql模板 'chunk_query.sql.j2' 不存在")
        except Exception as e:
            print(f"错误执行sql: {e}")
