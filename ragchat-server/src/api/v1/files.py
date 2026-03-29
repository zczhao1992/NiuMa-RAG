import os
import uuid
from dotenv import load_dotenv
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.api_contract import APIContract
from src.db.pg_db import get_db
from src.services.file_service import FileService
from src.services.chunk_service import ChunkService
from src.handler.partition_handler import PartitionHandler


load_dotenv()

upload_path = os.getenv('UPLOAD_PATH')


router = APIRouter(tags=['files'], prefix="/files")


ALLOWED_EXTENSIONS = [".docx", ".pdf", ".txt"]


@router.post("/")
async def upload_file(file: UploadFile = File(...), collection_id: str = Form(None), db: AsyncSession = Depends(get_db)):

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return APIContract.error(400, f"filename: {file.filename}, Unsupported file type. Only .docx and .pdf are allowed.")

    # 保存文件到服务器
    save_path = f"{upload_path}{file.filename}"

    try:
        with open(save_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        return APIContract.error(400, f"Failed to save file {file.filename}: {e}")

    file_service = FileService(db)

    # 存入数据库记录
    file_dto = await file_service.create(
        file_name=file.filename,
        uuid=uuid.uuid1(),
        collection_id=collection_id,
        file_extension=file_extension[1::],
        create_time=datetime.now(timezone.utc)
    )

    # 调用分块处理器
    part_handler = PartitionHandler()
    await part_handler.file_partition(
        file_id=file_dto.uuid,
        file_name=file.filename,
        file_path=save_path,
        file_extension=file_extension
    )

    return APIContract.success({"filename": file.filename, "message": "File store to chunk successfully."})


@router.get("/")
async def get_all(data: dict, db: AsyncSession = Depends(get_db)):
    service = FileService(db)
    return APIContract.success(await service.query_files(data.get("collection_id")))


@router.delete("/")
async def delete_file(data: dict, db: AsyncSession = Depends(get_db)):
    file_id = data.get("file_id")

    chunk_service = ChunkService(db)
    await chunk_service.delete_chunks_by_file_id(file_id)

    service = FileService(db)
    return APIContract.success(await service.delete_file(file_id))
