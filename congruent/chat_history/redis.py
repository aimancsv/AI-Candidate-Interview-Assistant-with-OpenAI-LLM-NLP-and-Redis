import json
import os
from typing import List
from fastapi.encoders import jsonable_encoder
import redis

redis_host = os.getenv("REDIS_HOST") or ""
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def append_dialogue(dialogue: List[dict], query: str, reply: str) -> List[dict]:
    return [
        *dialogue,
        {"role": "user", "content": query},
        {"role": "assistant", "content": reply},
    ]


def store_dialogue(
    session_key: str,
    query: str,
    reply: str,
    dialogue: List[dict] = [],
):
    try:
        updated_dialogue = append_dialogue(dialogue, query, reply)
        print("updated_dialogue ----->", updated_dialogue)
        serialized_dialogue = json.dumps(jsonable_encoder(updated_dialogue))
        redis_client.setex(f"{session_key}:dialogue", 3600, serialized_dialogue)
        return dialogue
    except Exception as e:
        print(f"Error in store_dialogue: {e}")
        raise


def retrieve_dialogue(key: str) -> List[dict]:
    try:
        raw_dialogue = redis_client.get(f"{key}:dialogue")

        if not raw_dialogue:
            return []

        parsed_dialogue = json.loads(raw_dialogue)
        return [
            {"role": msg["role"], "content": msg["content"]} for msg in parsed_dialogue
        ]
    except Exception as e:
        print(f"Error in retrieve_dialogue: {e}")
        return []


def erase_dialogue(key: str) -> bool:
    redis_client.delete(f"{key}:dialogue")
    return True
