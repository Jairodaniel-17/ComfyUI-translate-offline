from domain.translation_entity import TranslationResult


class TranslationUseCase:
    def __init__(self, translator_adapters, service, cache_service):
        """
        translator_adapters: dict of (src,tgt) -> adapter
        service: TranslationService
        cache_service: CacheService
        """
        self.adapters = translator_adapters
        self.service = service
        self._cache = cache_service

    def _direct_translate(self, adapter, text, src):
        # Construir chunks y traducir secuencialmente
        chunks = (
            self.service.build_chunks(
                text,
                adapter.tokenizer
                if hasattr(adapter, "tokenizer") and adapter.tokenizer
                else adapter._load() or adapter.tokenizer,
                src,
            )
            if hasattr(adapter, "tokenizer")
            else self.service.build_chunks(text, lambda s: s, src)
        )
        # Si el adapter no tiene tokenizer (porque no cargó aún), build_chunks fallará; fallback a dividir por oraciones
        if not chunks:
            chunks = self.service.split_text(text, src)
        translated = []
        for c in chunks:
            translated.append(adapter.translate_chunk(c))
        return " ".join(translated), chunks

    def execute(self, text: str, src: str, tgt: str) -> TranslationResult:
        # Normalizaciones rápidas
        text = (text or "").strip()
        if not text:
            return TranslationResult("", "", [])

        if src == tgt:
            return TranslationResult(text, text, [text])

        result = self._cache.get(text, src, tgt)
        if result:
            return result

        # 1) Intentar traducción directa src->tgt
        if (src, tgt) in self.adapters:
            adapter = self.adapters[(src, tgt)]
            translated_text, chunks = self._translate_using_adapter(adapter, text, src)
            result = TranslationResult(text, translated_text, chunks)
            self._cache.set(text, src, tgt, result)
            return result

        # 2) Si no existe directa, intentar pivot vía inglés: src->en->tgt
        if (
            src != "en"
            and tgt != "en"
            and (src, "en") in self.adapters
            and ("en", tgt) in self.adapters
        ):
            a1 = self.adapters[(src, "en")]
            mid_text, chunks1 = self._translate_using_adapter(a1, text, src)
            a2 = self.adapters[("en", tgt)]
            final_text, chunks2 = self._translate_using_adapter(a2, mid_text, "en")
            result = TranslationResult(text, final_text, chunks1 + chunks2)
            self._cache.set(text, src, tgt, result)
            return result

        # 3) Si no hay forma de traducir, devolver original
        result = TranslationResult(text, text, [text])
        self._cache.set(text, src, tgt, result)
        return result

    def _translate_using_adapter(self, adapter, text, src):
        # Intenta usar tokenize/constructor de chunks con el tokenizer del adapter si está disponible
        # Si adapter es LazyONNXTranslatorAdapter, se cargará dentro de translate_chunk en caso de ser necesario.
        # Para evitar depender del tokenizer en build_chunks (que puede no existir si no se ha cargado),
        # primero intentamos cargar tokenize info sin romper:
        tokenizer = getattr(adapter, "tokenizer", None)
        if tokenizer is None:
            # Forzamos carga ligera para disponer tokenizer; si falla, seguimos con split simple
            try:
                adapter._load()
                tokenizer = getattr(adapter, "tokenizer", None)
            except Exception:
                tokenizer = None

        if tokenizer:
            chunks = self.service.build_chunks(text, tokenizer, src)
        else:
            chunks = self.service.split_text(text, src)

        translated_chunks = []
        for c in chunks:
            translated_chunks.append(adapter.translate_chunk(c))
        translated_text = self.service.postprocess(" ".join(translated_chunks))
        return translated_text, chunks
