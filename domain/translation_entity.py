from dataclasses import dataclass
from typing import List


@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    chunks: List[str]
