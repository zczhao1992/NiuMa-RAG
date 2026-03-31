import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router
from src.core.embedding_manager import initialize_embeddings
from src.job.scheduler_setup import scheduled_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await initialize_embeddings()
    except Exception as e:
        raise

    task = asyncio.create_task(scheduled_job())

    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
