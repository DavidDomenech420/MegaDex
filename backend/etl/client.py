import hashlib
import json
import httpx
from pathlib import Path
from socket import timeout
from typing import Any

def fetch_json(url: str) -> dict[str, Any]:
    CACHE_DIR = Path(__file__).resolve().parent / ".cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{url_hash}.json"
    
    # Comprovamos si miramos informacion de la cache
    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    
    # Miramos en internet
    response = httpx.get(url, timeout=15.0)
    response.raise_for_status()
    data = response.json()
    
    # Guardamos la respuesta en la cache antes de devolverla
    with cache_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        
    return data