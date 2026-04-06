import asyncio
import uuid
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector
from src.core.embedding_manager import get_embeddings
from src.db.pg_db import get_db
from src.dto.embedding_dto import EmbeddingDto
from src.services.chunk_service import ChunkService
from src.services.embedding_service import EmbeddingService


async def do_embedding_chunks():
    # 从chunk表中获取，没有向量化的数据
    print("开始执行向量化任务...")  # 日志 1
    rows = []
    async for session in get_db():
        chunk_service = ChunkService(session)
        rows = await chunk_service.query_embedding_chunks()
        break

    if not rows:
        print("未发现 status=0 的数据，跳过。")  # 日志 2
        return []

    print(f"发现 {len(rows)} 条待处理数据，开始计算向量...")  # 日志 3

    embedding_model = get_embeddings()
    # 把content内容做向量化
    chunk_embedding_dict = await _create_embeddings(rows, embedding_model)

    print("向量计算完成，准备写入 embedding 表...")  # 日志 4

    # 组装dto数组
    embedding_dto_list = await _prepare_embedding_list(rows, chunk_embedding_dict)

    # 把向量的数据 插入到embedding表中
    async for session in get_db():
        embedding_service = EmbeddingService(session)
        print("DEBUG: 开始调用 batch_embedding_create...")  # 新增日志
        await embedding_service.batch_embedding_create(embedding_dto_list)
        print("DEBUG: batch_embedding_create 执行完毕！")  # 新增日志

        print("写入 embedding 成功，准备更新 chunk 状态...")  # 日志 5
        chunk_service = ChunkService(session)

        uuids = [row.chunk_id for row in rows]
        await chunk_service.batch_update_status_by_uuids(uuids, 1)
        print("整批任务处理完成并已提交事务！")  # 日志 6
        break


async def _prepare_embedding_list(chunk_embedding_dtos, embeddings_dict):
    print(f"DEBUG: 准备组装 DTO, 待处理数量: {len(chunk_embedding_dtos)}")
    embedding_dto_list = []

    for i, dto in enumerate(chunk_embedding_dtos):
        try:
            # 关键点：检查 ID 是否在字典里
            if dto.chunk_id not in embeddings_dict:
                print(f"警告: chunk_id {dto.chunk_id} 不在向量字典中！")
                continue

            embedding_dto = EmbeddingDto(
                uuid=uuid.uuid4(),
                chunk_id=dto.chunk_id,
                collection_id=dto.collection_id,
                file_id=dto.file_id,
                embedding_vector=Vector(embeddings_dict[dto.chunk_id]),
                search_vector=dto.context,
                create_time=datetime.now(timezone.utc)
            )
            embedding_dto_list.append(embedding_dto)
        except Exception as e:
            print(f"组装第 {i} 条数据时崩溃: {e}")
            raise e

    print(f"DEBUG: DTO 组装完成，实际生成数量: {len(embedding_dto_list)}")
    return embedding_dto_list


async def _create_embeddings(chunk_embedding_dtos, embedding_model):
    import time
    start_time = time.time()

    texts = [row.context for row in chunk_embedding_dtos]
    chunk_ids = [row.chunk_id for row in chunk_embedding_dtos]

    if not texts:
        return []

    embeddings = embedding_model.embed_documents(texts)

    embedding_dict = dict(zip(chunk_ids, embeddings))

    tatal_time = time.time() - start_time

    return embedding_dict


async def scheduled_job():
    try:
        while True:
            await do_embedding_chunks()
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        raise
