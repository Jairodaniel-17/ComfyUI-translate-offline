import re


class TranslationService:
    def __init__(self, sentence_splitter, chunk_size=400):
        self.sentence_splitter = sentence_splitter
        self.chunk_size = chunk_size

    def split_text(self, text, lang):
        return self.sentence_splitter.split(text, lang)

    def build_chunks(self, text, tokenizer, lang):
        sentences = self.split_text(text, lang)
        chunks, current = [], ""
        for s in sentences:
            potential = f"{current} {s}".strip()
            try:
                token_len = len(tokenizer.encode(potential))
            except Exception:
                # Si el tokenizer falla, usar longitud por caracteres como fallback
                token_len = len(potential)
            if token_len > self.chunk_size and current:
                chunks.append(current)
                current = s
            else:
                current = potential
        if current:
            chunks.append(current)
        return chunks

    def postprocess(self, text):
        return (
            text.replace(" .", ".")
            .replace(" ,", ",")
            .replace(" !", "!")
            .replace(" ?", "?")
            .strip()
        )

    # pequeño fallback de splitting simple (por si no hay nltk)
    @staticmethod
    def naive_sentence_split(text):
        return re.split(r"(?<=\.|\?|\!)\s", text)
