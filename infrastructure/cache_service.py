import json
import os
import sqlite3

from domain.translation_entity import TranslationResult


class CacheService:
    def __init__(self, db_path="test_cache.db"):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_path)
        print(f"CacheService init: db_path={self.db_path}, cwd={os.getcwd()}")
        self._init_db()

    def _init_db(self):
        print(f"Connecting to DB: {self.db_path}")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    text TEXT,
                    src_lang TEXT,
                    tgt_lang TEXT,
                    translated_text TEXT,
                    chunks TEXT,
                    PRIMARY KEY (text, src_lang, tgt_lang)
                )
            """)

    def get(self, text, src, tgt):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT translated_text, chunks FROM cache
                WHERE text = ? AND src_lang = ? AND tgt_lang = ?
            """,
                (text, src, tgt),
            )
            row = cursor.fetchone()
            if row:
                translated_text, chunks_json = row
                chunks = json.loads(chunks_json)
                return TranslationResult(text, translated_text, chunks)
        return None

    def set(self, text, src, tgt, result: TranslationResult):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache (text, src_lang, tgt_lang, translated_text, chunks)
                VALUES (?, ?, ?, ?, ?)
            """,
                (text, src, tgt, result.translated_text, json.dumps(result.chunks)),
            )
