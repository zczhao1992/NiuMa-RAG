import asyncio
from datetime import datetime, timezone
import uuid
from fastapi import Depends
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.dto.chunk_dto import ChunkDto
from src.db.pg_db import get_db
from src.services.chunk_service import ChunkService


class PartitionHandler:

    def __init__(self):
        pass

    async def file_partition(self, file_id, file_name, file_path, file_extension):
        try:
            if file_extension == ".docx":
                loader = Docx2txtLoader(file_path)
            elif file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_extension == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")

            docs = loader.load()

            # 创建文本分割器
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,  # 每个块的最大字符数，为300最佳
                chunk_overlap=50,  # 相邻块之间的重叠字符数为50最佳
                length_function=len,  # 计算文本长度的函数
                # add_start_index=True, # 是否添加起始索引
            )

            # Make splits
            split_docs = text_splitter.split_documents(docs)

            chunks_to_insert = []
            for i, doc in enumerate(split_docs):
                chunk_dto = ChunkDto(
                    uuid=uuid.uuid1(),
                    file_id=file_id,
                    file_name=file_name,
                    context=doc.page_content,
                    index=i,
                    status=0,
                    create_time=datetime.now(timezone.utc)
                )
                chunks_to_insert.append(chunk_dto)

            if not chunks_to_insert:
                return True

            # 分批次批量插入
            batch_size = 1000  # 每批插入的记录数
            total_chunks = len(chunks_to_insert)
            success_count = 0

            async for db in get_db():
                chunk_service = ChunkService(db)

                for i in range(0, total_chunks, batch_size):
                    batch = chunks_to_insert[i:i + batch_size]
                    batch_num = i // batch_size + 1
                    total_batchs = (
                        total_chunks + batch_size - 1) // batch_size

                    try:
                        await chunk_service.batch_create(batch)
                        success_count += len(batch)

                        await asyncio.sleep(0.1)

                        break
                    except Exception as e:
                        import traceback
                        traceback.print_exc()

        except FileNotFoundError:
            print(f"文件 {file_path} 未找到")
            return None
        except Exception as e:
            print(f"读取文件时发生错误：{e}")
            return None
