import os
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.file import File
from src.utils.sql_template_manager import SQLTemplateManager
from sqlalchemy import text


class FileDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, File, primary_key="uuid")
        self.sql_template_manager = SQLTemplateManager(
            os.path.dirname(__file__))

    async def query_files(self, collection_id: str):

        try:
            sql = self.sql_template_manager.render_sql(
                "sql/file_query.sql.j2", collection_id=collection_id)

            result = await self.db.execute(text(sql))

            # 获取所有行
            rows = result.all()
            columns = result.keys()

            data = [dict(zip(columns, row)) for row in rows]

            return data
        except FileNotFoundError:
            print(f"Error: SQL template file 'file_query.sql.j2' not found.")
        except Exception as e:
            print(f"Error excuting SQL: {e}")
        return []
