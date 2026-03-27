
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


class BaseDao:
    def __init__(self, db: AsyncSession, model, primary_key: str = "id"):
        """
        初始化 BaseDao
        : param db: 数据库会话
        : param model: 数据库模型
        : param primary_key: 主键字段名称，默认为 'id'
        """
        self.db = db
        self.model = model
        self.primary_key = primary_key

    async def create(self, **kwargs):
        """通用创建方法 """
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)

        return instance

    async def batch_create(self, objects: list):
        """通用批量创建方法"""
        instances = [self.model(**obj.dict()) for obj in objects]
        self.db.add_all(instances)
        await self.db.commit()
        # 可选：如果需要刷新实例可获取数据库生成的字段（如自增ID等）
        for instance in instances:
            await self.db.refresh(instance)

        return instances

    async def get_by_primary_key(self, key_value):
        """通过主键获取记录"""
        stmt = select(self.model).where(
            getattr(self.model, self.primary_key) == key_value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self):
        """获取所有"""
        stmt = select(self.model)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_by_primary_key(self, key_value, **kwargs):
        """通用更新方法"""
        stmt = (
            update(self.model)
            .where(getattr(self.model, self.primary_key) == key_value)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_by_primary_key(self, key_value):
        """通用删除方法"""
        stmt = delete(self.model).where(
            getattr(self.model, self.primary_key) == key_value)
        await self.db.execute(stmt)
        await self.db.commit()
        return True
