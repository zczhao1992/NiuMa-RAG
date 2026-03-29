import logging
import os
from dotenv import load_dotenv
from typing import List
import requests
from utils import show_toast


load_dotenv()

backend_url = os.getenv('BACKEND_URL')


async def create_collection(name: str):
    try:
        response = requests.post(
            backend_url + "collections/", json={"name": name})
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]
    except Exception as e:
        show_toast(f"创建{name} 记录失败：{e}", False)
    return None


async def update_collection(uuid: str, name: str):
    try:
        response = requests.put(
            backend_url + "collections/" + uuid, json={"name": name})
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]
    except Exception as e:
        show_toast(f"修改{name} 记录失败：{e}", False)
    return None


async def get_collection_by_id(uuid: str):
    try:
        response = requests.get(
            backend_url + "collections/" + uuid)
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"修改{uuid} 记录失败：{e}", False)
    return None


async def get_collections():
    try:
        response = requests.get(
            backend_url + "collections/")
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"获取记录失败：{e}", False)
    return None


async def delete_collection_by_id(uuid: str):
    try:
        response = requests.delete(
            backend_url + "collections/" + uuid)
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"删除{uuid} 记录失败：{e}", False)
    return None


async def get_files(collection_id: str):
    try:
        response = requests.get(
            backend_url + "files/", json={"collection_id": collection_id})
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"获取记录失败：{e}", False)
    return None


async def upload_file(collection_id: str, files):
    try:
        response = requests.post(
            backend_url + "files/", files=files, data={"collection_id": collection_id})
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"获取记录失败：{e}", False)
    return None


async def delete_file(file_id: str):
    try:
        response = requests.delete(
            backend_url + "files/", json={"file_id": file_id})
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"删除{file_id} 记录失败：{e}", False)
    return None


async def get_chunks(file_id: str):
    try:
        response = requests.get(
            backend_url + "chunks/file/" + file_id)
        if response.status_code != 200:
            show_toast(f"请求失败，状态码：{response.status_code}", False)
            return None

        try:
            result = response.json()
        except ValueError as e:
            show_toast(f"解析响应 JSON 失败：{e}", False)
            return None

        if result.get("code") == 0:
            return result["data"]

    except Exception as e:
        show_toast(f"获取记录失败：{e}", False)
    return None
