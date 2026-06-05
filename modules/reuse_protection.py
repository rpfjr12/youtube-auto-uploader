import hashlib
import json
from pathlib import Path
from typing import Dict, Optional

CACHE_PATH = Path("uploads/reuse_cache.json")


def _load_store() -> Dict[str, Dict[str, str]]:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text())
        except Exception:
            return {}
    return {}


def _save_store(store: Dict[str, Dict[str, str]]):
    CACHE_PATH.parent.mkdir(exist_ok=True)
    CACHE_PATH.write_text(json.dumps(store, indent=2))


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_duplicate(asset_type: str, fingerprint: str) -> bool:
    store = _load_store()
    return fingerprint in store.get(asset_type, {})


def register_asset(asset_type: str, fingerprint: str, metadata: Optional[Dict[str, str]] = None):
    store = _load_store()
    entry = store.setdefault(asset_type, {})
    if fingerprint in entry:
        return True
    entry[fingerprint] = metadata or {}
    _save_store(store)
    return False


def ensure_unique_script(script_dict: Dict[str, str], regenerate_func, max_attempts: int = 5) -> Dict[str, str]:
    attempt = 0
    while attempt < max_attempts:
        fingerprint = hash_text(script_dict.get("script_text", ""))
        if not is_duplicate("script", fingerprint):
            register_asset("script", fingerprint, {"topic": script_dict.get("topic", "unknown")})
            return script_dict
        attempt += 1
        script_dict = regenerate_func()
    register_asset("script", fingerprint, {"topic": script_dict.get("topic", "unknown"), "forced": "true"})
    return script_dict


def ensure_unique_metadata(title: str, description: str, tags: list, max_attempts: int = 5):
    from modules.randomization_engine import randomize_tag_order, randomize_description_blocks

    attempt = 0
    while attempt < max_attempts:
        fingerprint = hash_text(title + description + "|" + ",".join(tags))
        if not is_duplicate("metadata", fingerprint):
            register_asset("metadata", fingerprint, {"title": title})
            return title, description, tags
        attempt += 1
        tags = randomize_tag_order(tags)
        description = randomize_description_blocks(description)
        title = f"{title}"
    register_asset("metadata", fingerprint, {"title": title, "forced": "true"})
    return title, description, tags
