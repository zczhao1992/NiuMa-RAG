from langchain_huggingface import HuggingFaceEmbeddings
import torch

_embeddings = None


async def initialize_embeddings():
    global _embeddings
    try:
        # model_path = "D:/HuggingFace/bge-large-zh-v1.5"
        model_path = "BAAI/bge-small-zh-v1.5"
        # 检测设备
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # device = 'cpu'

        if device == "cuda":
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}
        else:
            model_kwargs = {
                "device": device,
                "trust_remote_code": True
            }
            encode_kwargs = {
                "normalize_embeddings": True,
                "batch_size": 32
            }
            import os
            if hasattr(torch, 'set_num_threads'):
                torch.set_num_threads(os.cpu_count())

        _embeddings = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

    except Exception as e:
        raise


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        raise RuntimeError("Embeddins 模版没有初始化，需要调用initialize_embeddings()")
    return _embeddings
