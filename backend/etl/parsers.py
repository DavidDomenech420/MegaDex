
from typing import Any


def extract_bilingual(entries: list[dict[str, Any]], value_key: str = "name") -> dict[str, str]:
    parsed: dict[str, str] = {}
    
    for entry in entries:
        # Miramos el lenguaje
        lang = entry.get("language", {}).get("name")
        if lang in ("es", "en") and lang not in parsed:
            parsed[lang] = entry[value_key]
    
    # Si no esta en español insertamos en ingles
    if "es" not in parsed and "en" in parsed:
        parsed["es"] = parsed["en"]
    
    return parsed

def clean_text(raw: str) -> str:
    normalized = raw.replace("\f", " ").replace("\n", " ")
    return " ".join(normalized.split())

def extract_game_flavor_text(entries: list[dict[str, Any]], game_pokeapi_slug: str) -> dict [str, str]:
    filtered_entries = [
        entry for entry in entries
        if entry.get("version", {}).get("name") == game_pokeapi_slug
    ]
    
    localized = extract_bilingual(filtered_entries, value_key="flavor_text")
    
    if not localized:
        return None

    return {lang: clean_text(text) for lang, text in localized.items()}