import re

import nltk
from nltk.tokenize import sent_tokenize

# Intentar descargar una vez; si falla no rompe import
try:
    nltk.download("punkt_tab", quiet=True)
    nltk.download("punkt", quiet=True)
except Exception:
    pass


class NLTKSentenceSplitter:
    def split(self, text, lang):
        try:
            language = {
                "es": "spanish",
                "en": "english",
                "fr": "french",
                "de": "german",
            }.get(lang, "english")
            return sent_tokenize(text, language=language)
        except Exception:
            # fallback simple
            return re.split(r"(?<=\.|\?|\!)\s", text)
